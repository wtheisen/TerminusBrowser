'''
Created on May 15, 2017

@author: yottudev@gmail.com
'''
from subprocess import call
import subprocess
import os
from threading import Thread
import threading
from PIL import Image, ImageDraw


class TermImage(threading.Thread):
    def __init__(self):
        Thread.__init__(self)

    def stream(self, bp, irc, source, subfile, subfile2=False):
        TermImage.display_webm(source, stream=True, wait=True, fullscreen=True, path="", subfile=subfile, subfile2=subfile2)
        irc.stop()
        bp.subtitle.append_to_subfile = False

    
    @staticmethod
    def run_w3mimgdisplay(w3m_args):
        try:
            # Binary (Part of Package w3m-img (Debian)) 
            w3m_bin="/usr/lib/w3m/w3mimgdisplay"
            
            # Source: Taymon https://stackoverflow.com/questions/13332268/python-subprocess-command-with-pipe
            ps = subprocess.Popen(('echo', w3m_args), stdout=subprocess.PIPE)
            output = subprocess.check_output((w3m_bin), stdin=ps.stdout)
            ps.wait()
            return output
        except:
            raise

    # Split and save image
    @staticmethod
    def image_split_h(image_in, image_out):
        with Image.open(image_in) as image:
            (image_x, image_y) = image.size
            image_top = image.copy().crop((0, 0, image_x, image_y/3))
            image_center = image.copy().crop((0, image_y/3, image_x, image_y/3*2))
            image_bottom = image.copy().crop((0, image_y/3*2, image_x, image_y))
        
        
        # Draw rectangle around center image
        draw_center = ImageDraw.Draw(image_center)
        draw_center.rectangle([0, 0, image_x-1, image_y/3-1], outline=(255,127,0))
        
        image_horiz = Image.new('RGB', (image_y*3, image_x/3))
        image_horiz.paste(image_top)
        image_horiz.paste(image_center, (image_x, 0))
        image_horiz.paste(image_bottom, (image_x*2, 0))

        image_horiz.save(image_out)
    
    @staticmethod
    def exec_cmd(full_cmd):
        if isinstance(full_cmd, list):
            with open(os.devnull, 'w') as f:
                return subprocess.Popen(full_cmd, stdout=f, stderr=subprocess.STDOUT)
        
    @staticmethod
    def display(filename, path="./"):
        ''' Display image in terminal using w3mimgdisplay'''
        try:
            # Source for figuring out w3m_args: z3bra http://blog.z3bra.org/2014/01/images-in-terminal.html
            # args for getting the image dimensions
            w3m_args="5;" + path+filename
            xy = TermImage.run_w3mimgdisplay(w3m_args)
            x, y = xy.split()
            
            w3m_args="0;1;0;0;" + str(x) + ";" + str(y) + ";;;;;" + path+filename + "\n4;\n3;"
            TermImage.run_w3mimgdisplay(w3m_args)
        except:
            raise
        
    @staticmethod
    def display_ext(filename, **kwargs):
        ''' Automatically chooses best external viewer (hopefully) '''
        
        # get file extension from filename
        file_ext = filename.split(".").pop().lower()
        
        if file_ext == "jpg" or file_ext == "png":
            TermImage.display_img(filename, **kwargs)
            
        elif file_ext == "gif":
            TermImage.display_gif(filename, **kwargs)
            
        elif file_ext == "webm":
            TermImage.display_webm(filename, **kwargs)
        
        else:
            raise LookupError("No viewer for file extension configured: " + file_ext)
    
    @staticmethod        
    def display_img(filename, fullscreen=False, path="./", setbg=False):
        
        try:
            cmd = "feh"
            default_options = ['-q'] # quiet
            
            options = ['--auto-zoom']
            if fullscreen:
                options += ['-D-5', '-F'] # -D-5=Slideshow delay, -F=fullscreen
            
            options.append('--start-at') # 
            options_post = [path] # needed to browse other images in path
            
            if setbg:
                options = ['--bg-max']
                options_post = []
            
            full_cmd = [cmd] + default_options + options + [path+filename] + options_post
            
            TermImage.exec_cmd(full_cmd)
            return
            
            
        except:
            raise
        
    @staticmethod        
    def display_webm(filename, fullscreen=False, path="./", subfile=False, subfile2=False, wait=True, stream=False, **unused):
        ''' Returns: (stdoutdata, stderrdata)'''
        
        # The local directory path when streaming from an URL is not needed
        if stream:
            path = ""
            
        try:
            cmd = "mpv"
            default_options = ['--no-terminal']
            options = []
            if fullscreen:
                options.append('-fs')
                
            if subfile:
                options.append('--sub-file=' + str(subfile))
            if subfile2: # FIXME use a list
                options.append('--sub-file=' + str(subfile2))
                
            if stream:
                # lua script to continuously re-read the subfile
                options.append('--script=' + './lib/mpv-sub-reload.lua')
            
            full_cmd = [cmd] + default_options + options + [path+filename]
            
            proc = TermImage.exec_cmd(full_cmd)
            if wait:
                proc.wait()
            return
        
        except:
            raise
            
    @staticmethod        
    def display_gif(filename, fullscreen=False, path="./", **unused):
        ''' Returns: (stdoutdata, stderrdata)'''
        try:
            cmd = "sxiv"
            default_options = ['-q', '-a'] # quiet, play animations
            
            
            options = []
            if fullscreen:
                options = ['-f', '-sf', '-S1'] # fullscreen, scale to fit screen, loop
            
            full_cmd = [cmd] + default_options + options + [path+filename]
            
            TermImage.exec_cmd(full_cmd)
            return
            
        except:
            raise
            
