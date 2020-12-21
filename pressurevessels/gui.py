# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2020 tamalone1
"""
import tkinter as tk
from .PressureVessels import Vessel

# GUI class to create and manage the GUI
class PV_GUI(tk.Frame):
    # Create a GUI to interactively calculate pressure vessel stresses
    inputfields = ('External pressure',
                   'Internal pressure',
                   'Outer diameter',
                   'Inner diameter',
                   'Allowable stress')

    outputfields = ('Average Linear Stress',
                    'Maximum Local Stress',
                    'Internal Pressure for Burst',
                    'External Pressure for Collapse',
                    'Minimum Safety Factor')
                    
    defaultvalues = (15, 0, 1.695, 1.460, 120)

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # self.configure(background='gainsboro')

        # Create a vessel instance for the calculations
        self.vessel = Vessel(*self.defaultvalues)

        # Create the input entry fields
        inputframe = tk.Frame(self, background=self['background'])
        self.ent = self.buildinputtable(inputframe)
        inputframe.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Create the output table
        outputframe = tk.Frame(self, background=self['background'])
        self.outputs = self.buildoutputtable(outputframe)
        outputframe.grid(row=2, column=0, columnspan=2, padx=10, pady=10,
                         sticky='nsew')

        # Frame to contain the buttons
        buttonrowframe = tk.Frame(self, background=self['background'])
        # Insert calculate button
        calc_button = tk.Button(buttonrowframe, text='Calculate', width=20,
                                command=self.calculate_button_command)
        calc_button.pack(side=tk.LEFT, padx=10)
        # Insert button for minimize_OD
        minimizeOD_button = tk.Button(buttonrowframe, text='Minimum OD',
                                      width=20, command=self.minimize_OD)
        minimizeOD_button.pack(side=tk.LEFT, padx=10)
        # Insert button for minimize_OD
        maximizeID_button = tk.Button(buttonrowframe, text='Maximum ID',
                                      width=20, command=self.maximize_ID)
        maximizeID_button.pack(side=tk.LEFT, padx=10)
        # Grid the buttons
        buttonrowframe.grid(row=1, column=0, columnspan=2, padx=10, pady=10,
                            sticky='nsew')

        # Set the focus to the first entry box
        self.ent['External pressure'].focus_set()

    def entryhighlight(self, event):
        # Change entry color to indicate hovering over it
        event.widget['background'] = 'honeydew'
        event.widget['foreground'] = '#000000'

    def entryrevert(self, event):
        # Change entry color after moving off of entry
        event.widget['background'] = 'white'
        event.widget['foreground'] = '#05322B'

    def buildinputtable(self, root):
        # Display entry boxes for each inputfield
        # Return dictionary of inputfield:entry pairs
        entries = {}
        for i, field in enumerate(self.inputfields):
            lab = tk.Label(root, width=20, text=field + ': ', anchor='e',
                           font=('Arial 12'), background=self['background'])
            lab.grid(row=i, column=0, padx=2, pady=2)
            ent = tk.Entry(root, width=20, font=('Arial 12'),
                           justify=tk.CENTER, foreground='#05322B')
            ent.insert(0, self.defaultvalues[i])
            ent.bind('<Enter>', self.entryhighlight)
            ent.bind('<Leave>', self.entryrevert)
            ent.grid(row=i, column=1, padx=2, pady=2)

            entries[field] = ent

        return entries

    def buildoutputtable(self, root):
        # Build the output table and store the label objects used to display
        # the values
        # outputrow1 = len(inputfields) + 2

        # Assemble output table header
        lab = tk.Label(root, width=20, text='Calculated Stress:', anchor='c',
                       font=('Arial 12'), background=self['background'])
        lab.grid(row=0, column=1, padx=2, pady=2)
        lab = tk.Label(root, width=20, text='Allowable Stress:', anchor='c',
                       font=('Arial 12'), background=self['background'])
        lab.grid(row=0, column=2, padx=2, pady=2)

        # Assemble output table
        outputs = {}
        for i, field in enumerate(self.outputfields):
            # Store the created labels in a dictionary for later
            outputs[field] = {}
            # Skip the first two rows (already built)
            currentrow = i + 1
            # First label is the actual field name
            lab = tk.Label(root, text=field+': ', anchor='e',
                           font=('Arial 12'), background=self['background'])
            # These fields will show additional values in the first column
            if field in ('Average Linear Stress', 'Maximum Local Stress'):
                # if data in column 1, place label as normal in column 0
                lab.grid(row=currentrow, column=0, padx=2, pady=2)
                lab = tk.Label(root, width=20, text='0', anchor='c',
                               relief=tk.GROOVE, font=('Arial 12'),
                               background=self['background'])
                lab.grid(row=currentrow, column=1, padx=2, pady=2)
                # For each field, store the label in a corresponding subfield
                outputs[field]['calculated'] = lab
            else:
                # If no data in column 1, make the label span columns 0 and 1
                lab.grid(row=currentrow, column=0, padx=2, pady=2,
                         columnspan=2)

            # All fields will show values in columns 2 and 3
            lab = tk.Label(root, width=20, text='0', anchor='c',
                           relief=tk.GROOVE, font=('Arial 12'),
                           background=self['background'])
            lab.grid(row=currentrow, column=2, padx=2, pady=2)
            # For each field, store the label in a corresponding subfield
            outputs[field]['allowable'] = lab

        # for each key in the outputs dictionary, the value is a
        # sub-dictionary containing the label objects for each column
        return outputs

    def get_entryvalues(self):
        # Get values from the entry boxes and return a dictionary of floats
        values = {}
        for fieldname, entrybox in self.ent.items():
            try:
                values[fieldname] = float(entrybox.get())
            except:
                # if the entry box is empty or not a number, use zero instead
                values[fieldname] = 0
                # display zero in the entry box
                entrybox.delete(0, tk.END)
                entrybox.insert(0, '0')

        # Assign the values to instance attributes
        self.vessel.pExt = values['External pressure']
        self.vessel.pInt = values['Internal pressure']
        self.vessel.OD = values['Outer diameter']
        self.vessel.ID = values['Inner diameter']
        self.vessel.allowable_stress = values['Allowable stress']

    def update_results(self):
        # self.get_entryvalues()
        # self.vessel.calculate()

        # Check the safety factors, and select the display color
        if self.vessel.SF < 1.00:
            SF_color = '#ff8888'
        else:
            SF_color = '#02BC94'


        # Get the new results and display them in the output table
        self.outputs['Average Linear Stress']['calculated'].configure(
                text='{:,.1f}'.format(self.vessel.averagestress))
        self.outputs['Average Linear Stress']['allowable'].configure(
                text='{:,.0f}'.format(self.vessel.allowable_stress*self.vessel.k))

        self.outputs['Maximum Local Stress']['calculated'].configure(
                text='{:,.1f}'.format(self.vessel.maxstress))
        self.outputs['Maximum Local Stress']['allowable'].configure(
                text='{:,.0f}'.format(self.vessel.allowable_stress))

        self.outputs['Minimum Safety Factor']['allowable'].configure(
                text='{:,.3f}'.format(self.vessel.SF),
                background=SF_color,
                foreground='white')

        self.outputs['Internal Pressure for Burst']['allowable'].configure(
                text='{:,.3f}'.format(self.vessel.maxInternal))
        self.outputs['External Pressure for Collapse']['allowable'].configure(
                text='{:,.3f}'.format(self.vessel.maxExternal))

    def calculate_button_command(self):
        ''' Get the current inputs, calculate, and update the output table.'''
        self.get_entryvalues()
        self.vessel.calculate()
        self.update_results()

    def minimize_OD(self):
        ''' Find the minimum OD with safety factor >= 1. 
        
        Uses the corresponding vessel method.'''
        # Get the inputs from the entry boxes and calculate
        self.get_entryvalues()
        self.vessel.calculate()
        # Call the vessel method
        self.vessel.minimize_OD()
        # Change the OD entrybox to show the new OD
        new_OD = self.vessel.OD
        self.ent['Outer diameter'].delete(0, tk.END)
        self.ent['Outer diameter'].insert(0, f'{new_OD:.3f}')
        # Update the results table with the calculated values
        self.update_results()

    def maximize_ID(self):
        ''' Find the maximum ID with safety factor >= 1. 
        
        Uses the corresponding vessel method.'''
        # Get the inputs from the entry boxes and calculate
        self.get_entryvalues()
        self.vessel.calculate()
        # Call the vessel method
        self.vessel.minimize_ID()
        # Change the OD entrybox to show the new OD
        new_ID = self.vessel.ID
        self.ent['Inner diameter'].delete(0, tk.END)
        self.ent['Inner diameter'].insert(0, f'{new_ID:.3f}')
        # Update the results table with the calculated values
        self.update_results()

def check_diameters(vessel, new_ID, new_OD):
    """ Change the vessel's ID and OD and return the resulting safety factor.
    """
    if new_OD <= new_ID:
        # OD must be larger than ID by any finite amount
        # Otherwise, don't try calculating, may cause error
        return 0
    else:
        vessel.modify_parameters(ID=new_ID, OD=new_OD)
        return vessel.SF
