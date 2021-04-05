import io,re,os
import tkinter as tk
import tkinter.ttk as ttk
import tkentrycomplete as tkec
import webbrowser

class DomainFinder():
	def __init__(self):
		HEIGHT = 809
		WIDTH= 500
		font=('Helvetica', 14)
		# ~ APP
		self.app = tk.Tk()
		# ~ STYLE
		ttk.Style().theme_use('classic')
		# ~ FRAME & BASIC SUTFF 
		self.frame = tk.Frame(self.app)
		self.app.title('Clever domain name helper')
		self.frame.grid()
		
		# ~ which extension list do we take (which provider)
		self.extension_folder="extension_lists"
		self.extension_lists=[re.sub(r"_.*","",r) for r in os.listdir(self.extension_folder)]
		self.TLD_providers_var = tk.StringVar()
		self.TLD_providers_var.set(self.extension_lists[0])
		self.TLD_list = tk.OptionMenu(self.frame,self.TLD_providers_var,*self.extension_lists,command=self.change_list)
		self.TLD_list.grid(row=0,column=0,sticky="nw")
		

		# ~ search list of extensions with autocomplete 
		self.TLD_entry = tkec.AutocompleteCombobox(self.frame,textvariable=tk.StringVar())
		self.TLD_entry.grid(row=0,column=1,sticky="n")
		self.change_list()
		
		# ~ binding the search to the combobox
		self.TLD_search= tk.Button(self.frame, 
				text="search", 
				font=font,
				command=self.reload_domains)
		self.TLD_search.grid(row=0,column=2,sticky="ne")
		
		# ~ ah yes the scrollbar
		self.scrollbar=tk.Scrollbar(self.frame,orient=tk.VERTICAL)
		self.scrollbar.grid(column=3,sticky='ns')
		

		# ~ show the results in a list
		
		self.lb = tk.Listbox(self.frame, listvariable=tk.StringVar(),width=50,height=20,font=font,bd=10,)
		self.lb.configure(yscrollcommand=self.scrollbar.set)
		self.lb.bind('<Double-Button-1>', self.visit_website)
		
		
		# ~ bind the scrollbar
		self.scrollbar.config(command=self.lb.yview)
		self.data = io.open("words/words-en.txt","r",encoding="utf8").read().splitlines()
		
		
		# ~ launch 
		self.reload_domains()
		self.app.mainloop()
	
	def visit_website(self,value):
		address=self.lb.get(tk.ACTIVE)
		webbrowser.open("https://{}".format(address))
	
	def change_list(self,choice=None):
		if choice == None:
			choice=self.extension_lists[0]
		extension_list = io.open("{}/{}_extensions.txt".format(self.extension_folder,choice),"r",encoding="utf8").read().splitlines()
		self.TLD_entry.set_completion_list(extension_list)
	
	def reload_domains(self):
		tld=self.TLD_entry.get()
		if tld=="":
			tld = "ch"
		self.lb.delete(0, tk.END)
		domains = self.get_domains(tld)
		for d in domains:
			self.lb.insert(tk.END,d)
			self.lb.itemconfig(tk.END, bg = 'white' if self.lb.size() % 2 == 0 else 'light grey')
		self.lb.grid(row=1,columnspan=3)
		self.lb.configure(yscrollcommand=self.scrollbar.set)
		
	def get_domains(self,tld):
		r = re.compile(".{{5,}}{}$".format(tld))
		domains = list(filter(r.match,self.data))
		domains = [re.sub("{}$".format(tld),".{}".format(tld),s) for s in domains]
		if domains == []:
			return ["No match, sorry"]
		return domains
	
	def run(self):	
		self.app.update()
		for i in range(0,len(text)):
			line.insert('1.0',text[len(text)-1-i])
			
		
if __name__ == '__main__':
	df = DomainFinder()