#!/usr/bin/env python

# Figure 1: UV-Vis data

import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = './UV VIS SPECTRUM.xlsx'
data = pd.read_excel(file_path, sheet_name=None)

# Load the data from the relevant sheet
sheet_name = 'Row 1 - Row 17'

# Skip metadata rows and load actual data
df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=10)

# Display the first few rows of actual data
#df.head()

# get rid of first column
df = df.drop(columns=['Unnamed: 0'])

# Rename columns for easier access and display
df.columns = ['Wavelength (nm)', 'Sample 1a UF', 'Sample 1b UF', 'Sample 1a F', 'Sample 1b F',
              'Sample 2a UF', 'Sample 2b UF', 'Sample 2a F', 'Sample 2b F', 'Sample 3a UF', 
              'Sample 3b UF', 'Sample 3a F', 'Sample 3b F', 'Sample 4a UF', 'Sample 4b UF', 
              'Sample 4a F', 'Sample 4b F']

# Remove non-numeric rows
df = df[pd.to_numeric(df['Wavelength (nm)'], errors='coerce').notnull()]

# Convert data to floating point values
df = df.astype(float)

# List of samples
samples = df.columns[1:]

# Plot the data
fig, axes = plt.subplots(4, 4, figsize=(20, 20))
axes = axes.flatten()


# Determine the global y-axis limits so that we can plot all of the
# small multiples at the same scale (Tufte E., 1983; Tufte E., 1990)

y_min = df[samples].min().min()
y_max = df[samples].max().max()

# plot a 4x4 grid
for i, sample in enumerate(samples):
    wavelengths = df['Wavelength (nm)']
    absorbance = df[sample]
    peak_wavelength = wavelengths[absorbance.idxmax()]
    
    axes[i].plot(wavelengths, absorbance, label=sample)
    axes[i].axvline(x=peak_wavelength, color='r', linestyle='--')
    # Position the label slightly to the right of the peak with a small margin on the left-hand side
    axes[i].text(peak_wavelength + 10, y_min + (y_max - y_min) * 0.05, f'peak: {peak_wavelength:.0f} nm', 
                 verticalalignment='bottom', horizontalalignment='left', rotation=0)
    axes[i].set_title(sample)
    axes[i].set_xlabel('Wavelength (nm)')
    axes[i].set_ylabel('Absorbance')
    axes[i].set_ylim(y_min, y_max)
    axes[i].legend()

plt.tight_layout()
#plt.show()
fig.savefig("fig1.svg", format='svg')

# Tufte, Edward (1983). Visual Display of Quantitative Information. Graphics Press. ISBN 978-1930824133.
# Tufte, Edward (1990). Envisioning Information. Graphics Press. p. 67. ISBN 978-0961392116.
