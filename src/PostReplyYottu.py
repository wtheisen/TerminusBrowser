'''
Created on May 15, 2017

@author: yottudev@gmail.com
This class is used to handle posting replies including retrieving and displaying the captcha.
2018-03-17: removed v1 support and replaced it with v2 fallback
'''

import mimetypes
import os.path
import re
import thread
import time
import warnings

import requests
from bs4 import BeautifulSoup
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
from DebugLog import DebugLog
from TermImage import TermImage

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

class PostReply(object):
    '''
    classdocs
    '''

    def __init__(self, board, threadno):
        self.board = board
        self.threadno = threadno
        
        self.sitekey = "6Ldp2bsSAAAAAAJ5uyx_lx34lJeEpTLVkP5k04qc"

        self.captcha2_url = "https://www.google.com/recaptcha/api/fallback?k=" + self.sitekey
        self.captcha2_payload_url = "https://www.google.com/recaptcha/api2/payload"
        self.captcha2_image_base_url = ""
        self.site_ref = "https://boards.4chan.org/"
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0'
        
        self.captcha2_challenge_text = None # "Select all images with ducks."
        self.captcha2_challenge_id = None
        
        self.captcha2_image = "" # Binary image
        self.captcha2_image_filename = "yottu-captcha.jpg" # TODO don't save the image
        
        self.captcha2_solution = None # Array of integers associated to the captcha checkboxes, usually 0-8
        self.captcha2_response = None # Response the Reply post form wants (the actual solution)
        
        self.lock = thread.allocate_lock()
        self.dictOutput = None
        self.bp = None 
        
        self.dlog = DebugLog()
        
    class PostError(Exception):
        def __init__(self,*args,**kwargs):
            Exception.__init__(self,*args,**kwargs)

#    def get_captcha_solution(self):
#        return self.__captcha_solution


    def set_captcha2_solution(self, value):
        # Append checkbox integer values to response array
        try:
            self.captcha2_solution = []
            for i in str(value):
                self.captcha2_solution.append(str(int(i) - 1))
        except ValueError as err:
            self.dlog.excpt(err, msg=">>>in PostReply.set_captcha2_solution()", cn=self.__class__.__name__)
            raise
        except Exception as err:
            self.dlog.excpt(err, msg=">>>in PostReply.set_captcha2_solution()", cn=self.__class__.__name__)


    def _query(self):
        pass

    def get_captcha_challenge(self):
        """
            1. Query captcha url with site key
            2. From the result get
                a) the challenge text
                b) the challenge id 
            3. Query payload url with site key and cid and get
                c) the captcha image
        """
        try:
            headers = {'Referer': self.site_ref, 'User-Agent': self.user_agent}
            r = requests.get(self.captcha2_url, headers=headers)
            
            r.raise_for_status()

            html_content = r.content
            soup = BeautifulSoup(html_content, 'html.parser')
            
            try:
                self.captcha2_challenge_text = soup.find("div", {'class': 'rc-imageselect-desc-no-canonical'}).text
            except:
                self.captcha2_challenge_text = soup.find("div", {'class': 'rc-imageselect-desc'}).text
                
            self.captcha2_challenge_id = soup.find("div", {'class': 'fbc-imageselect-challenge'}).find('input')['value']
            
            # Get captcha image
            headers = {'Referer': self.captcha2_url, 'User-Agent': self.user_agent}
            r = requests.get(self.captcha2_payload_url + '?c=' + self.captcha2_challenge_id + '&k=' + self.sitekey, headers=headers)
            self.captcha2_image = r.content
            #self.save_image(self.captcha2_image_filename)
            
        except Exception as err:
            self.dlog.excpt(err, msg=">>>in PostReply.get_captcha_challenge()", cn=self.__class__.__name__)
            raise
        
    def save_image(self, filename):
        """save image to file system"""
        try:
        
            with open(filename, "w") as f:
                f.write(self.captcha2_image)
            
        except Exception as err:
            self.dlog.excpt(err, msg=">>>in PostReply.save_image()", cn=self.__class__.__name__)

    def display_captcha(self):
        
        # Reformat picture to be displayed horizontally
        try:
            TermImage.image_split_h(StringIO(self.captcha2_image), self.captcha2_image_filename)
        except Exception as err:
            self.dlog.warn(err, msg=">>>in PostReply.display_captcha()", cn=self.__class__.__name__)
        
        # Overlay the captcha in the terminal
        try:
            TermImage.display(self.captcha2_image_filename)
            return True
        except:
            pass
        # On failure fall back to using the external image viewer
        try:
            TermImage.display_img(self.captcha2_image_filename)
            return False
        except:
            raise
    
    # FIXME captchav2 update
    def defer(self, time_wait, **kwargs):
        ''' wait for timer to run out before posting '''
        
        if not self.bp.cfg.get('user.pass.enabled'):
            self.get_response()
            captcha2_response = self.captcha2_response
            self.dlog.msg("Waiting C: " + captcha2_response[:12] + str(kwargs), 4)
        self.bp.sb.setStatus("Deferring comment: " + str(time_wait) + "s")
        
        
        self.lock.acquire()
        self.dlog.msg("Lock acquired for deferred post " + str(kwargs))
        
        try:   
            while time_wait > 0:
                time.sleep(time_wait)
                # get new lastpost value and see if post needs to be deferred further
                time_wait = self.bp.time_last_posted_thread + 60 - int(time.time()) 
            
            if not self.bp.cfg.get('user.pass.enabled'):
                kwargs.update(dict(captcha2_response=captcha2_response))
                self.dlog.msg("Now posting: C: " + captcha2_response[:12] + str(kwargs), 4)
            else:
                self.dlog.msg("Now posting deferred comment", 4)
            
            rc = self.post(**kwargs)
            if rc != 200:
                self.bp.sb.setStatus("Deferred comment was not posted: " + str(rc))
        except Exception as err:
            self.bp.sb.setStatus("Deferred: " + str(err))
        finally:
            self.lock.release()
     
     
    def get_response(self):
        
        try:
            
            headers = {'Referer': self.captcha2_url, 'User-Agent': self.user_agent}
            data={'c':self.captcha2_challenge_id, 'response':self.captcha2_solution}
            r = requests.post(self.captcha2_url, headers=headers, data=data)
            html_post = r.content
            soup = BeautifulSoup(html_post, 'html.parser')
        
        except Exception as err:
            self.dlog.excpt(err, msg=">>>in PostReply.get_response()", cn=self.__class__.__name__)
            raise
        
        
        try:
            self.captcha2_response = soup.find("div", {'class': 'fbc-verification-token'}).text
        except AttributeError as err:
            self.dlog.warn(err, msg="Could not get verification token, captcha input error (input: " + str(self.captcha2_solution) + ")?", cn=self.__class__.__name__)
            raise
        except Exception as err:
            self.dlog.excpt(err, msg=">>>in PostReply.get_response()", cn=self.__class__.__name__)


    def auth(self):
        # Set user.pass.cookie by posting the auth form containing user.pass.token and user.pass.pin

        try:
            token = self.bp.cfg.get('user.pass.token')
            pin = self.bp.cfg.get('user.pass.pin')
            if not token:
                token = self.bp.query_userinput(label="Token: ", input_type='text')

            if not pin:
                pin = self.bp.query_userinput(label="PIN: ", input_type='number')

            self.dlog.msg("Authenticating Pass with PIN/Token length: " + str(len(pin)) + "/" + str(len(token)), 3)

            data = dict(act='do_login', id=token, pin=pin)

            res = requests.post('https://sys.4chan.org/auth', data=data)

            self.bp.cfg.set('user.pass.cookie', res.cookies['pass_id'])

            if self.bp.cfg.get('config.autosave'):
				self.dlog.msg("Autosaving user.pass.cookie ..")
				self.bp.cfg.writeConfig()

        except KeyError as err:
            self.dlog.excpt(err, msg=">>>in PostReply.auth()", cn=self.__class__.__name__)
            raise PostReply.PostError("Could not authenticate pass token/pin.")
        except Exception as err:
            self.dlog.excpt(err, msg=">>>in PostReply.auth()", cn=self.__class__.__name__)



    def post(self, nickname="", comment="", subject="", file_attach="", ranger=False, captcha2_response=""):
        '''
        subject: not implemented
        file_attach: (/path/to/file.ext) will be uploaded as "file" + extension
        ranger: extract path from ranger's --choosefile file
        '''
        cookies = None
        try:
            if self.bp.cfg.get('user.pass.enabled'):

                if not self.bp.cfg.get('user.pass.cookie'):
                    # get and set new cookie from pass and pin
                    self.auth()
                cookies = dict(pass_id=self.bp.cfg.get('user.pass.cookie'),pass_enabled="1")

            elif not captcha2_response:
                    self.get_response()
                    captcha2_response = self.captcha2_response
                
            if nickname == None:
                nickname = ""
            else:
                nickname = u''.join(nickname)
            
            # Read file / get mime type
            try:
                if file_attach:
                    
                    # extract file path from ranger file and re-assign it
                    if ranger:
                        with open(file_attach, "r") as f:
                            file_attach = f.read()
                    
                    _, file_ext = os.path.splitext(file_attach)
                    filename = "file" + file_ext
                    content_type, _ = mimetypes.guess_type(filename)
                    with open(file_attach, "rb") as f:
                        filedata = f.read()
                        
                    if content_type is None:
                        raise TypeError("Could not detect mime type of file " + str(filename))
                else:
                    filename = filedata = content_type = ""
            except Exception as err:
                self.dlog.excpt(err, msg=">>>in PostReply.post() -> file_attach", cn=self.__class__.__name__)
                raise
    
            
            url = "https://sys.4chan.org/" + self.board + "/post"
            #url = 'http://httpbin.org/status/404'
            #url = "http://localhost/" + self.board + "/post"
            #url = 'http://httpbin.org/post'
            #url = 'http://requestbin.fullcontact.com/1i28ed51'
    
    
            values = { 'MAX_FILE_SIZE' : (None, '4194304'),
                       'mode' : (None, 'regist'),
                       # 'pwd' : ('', 'tefF92alij2j'),
                       'name' : (None, nickname),
                       # 'sub' : ('', ''),
                       'resto' : (None, str(self.threadno)),
                       # 'email' : ('', ''),
                       'com' : (None, comment),
                       'g-recaptcha-response' : (None, captcha2_response),
                       'upfile' : (filename, filedata, content_type)
                     }
            
            headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64)' }

            response = requests.post(url, headers=headers, files=values, cookies=cookies)
            
            # raise exception on error code
            response.raise_for_status()
            if re.search("is_error = \"true\"", response.text):
                perror = "Unknown Error."
                
                if self.bp.cfg.get('user.pass.cookie'):
                    perror += " user.pass.cookie might be invalid."
                try:
                    perror = re.search(r"Error: ([A-Za-z.,]\w*\s*)+", response.text).group(0)
                except:
                    if re.search("blocked due to abuse", response.text):
                        perror = "You are range banned ;_;"
                finally:
                    raise PostReply.PostError(perror)
            
            if response.status_code == 200 and self.dictOutput:
                self.dictOutput.mark(comment)
                self.bp.post_success(int(time.time()))
            else:
                self.dlog.msg("response.status_code: " + str(response.status_code))
                self.dlog.msg("self.dictOutput: " + str(self.dictOutput))
            
            
            return response.status_code
        
        except Exception as err:
            self.dlog.excpt(err, msg=">>>in PostReply.post()", cn=self.__class__.__name__)
            raise
