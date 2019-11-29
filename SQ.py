import os
import sys
import sublime
import sublime_plugin
import re
import json
from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError, errors
from os.path import basename, splitext

sqattop = 1;

class sqopenincludeCommand(sublime_plugin.WindowCommand):

	def run(self):
		print("openInclude");
		view = self.window.active_view()
		word = view.line(view.sel()[0])
		wordtext = view.substr(word)
		print(wordtext)

class sqformatcodeCommand(sublime_plugin.TextCommand):

	def __init__(self,view):
		  self.view=view;
		  self.language=self.get_language()

	def get_language(self):
		syntax = self.view.settings().get('syntax')
		language = splitext(basename(syntax))[0].lower() if syntax is not None else "plain text"
		return language

	def get_text_type(self):
		language = self.language;
		#print(language);
		if language == 'xml':
			return 'xml'
		if language == 'json':
			return 'json'
		if language == 'php':
		 	return 'php'
		if language == 'c++':
		 	return 'c++'
		if language == 'c':
		 	return 'c++'
		if language == "merlin":
			return "merlin"
		if language == 'plain text' and s:
			if s[0] == '<':
				return 'xml'
				if s[0] == '{' or s[0] == '[':
					return 'json'
		return 'notsupported'

	def run(self,edit):
		text_type = self.get_text_type();
		#print(text_type);
		if (text_type == 'php') :
			print('phpfmt')
			self.view.run_command("fmt_now")
		if (text_type == 'c++') :
			print('astyleformat');
			self.view.run_command("astyleformat")
		if (text_type == 'json') :
			print('IndentXML')
			self.view.run_command("auto_indent")
			self.view.run_command("json_comma")
			self.view.run_command("pretty_json")
		if (text_type == 'xml') :
			print('IndentXML')
			self.view.run_command("auto_indent")
		if (text_type == 'merlin') :
			print('syn: merlin')
			self.view.run_command("sqmerlin")

class sqfindCommand(sublime_plugin.WindowCommand):

	def run(self):
		global sqattop;
		if (sqattop != 0 ) :
			sqattop=0;
			self.window.run_command("show_panel", {"panel": "find", "reverse": False});
		else:
			self.window.run_command("hide_panel", {"panel": "find", "reverse": False});
			self.window.run_command("find_next");
			sqattop=0;

class sqconsoleCommand(sublime_plugin.WindowCommand):

	def run(self):
		self.window.run_command("show_panel", {"panel": "console", "toggle": True});

class sqbeginCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		global sqattop;
		self.view.run_command("move_to", {"to": "bof", "extend": False});
		sqattop=1;

class sqselectCommand(sublime_plugin.WindowCommand):

	def run(self):
		global sqattop;
		window=self.window;
		view=window.active_view();
		sel=view.sel();
		region=sel[0];
		sz=region.size();
		if (sz>0) :
		  view.run_command("expand_selection", {"to": "line"})
		else:
		  view.run_command("move", {"by": "pages", "forward": True});
	
class sqcloseotherCommand(sublime_plugin.WindowCommand):
  def run(self):
  	self.run_command("toggle_side_bar");