# Generate iTOL annotations

It works on passing a .csv file that looks something like this, i.e. there is a column that matches the labels you have in your nwk file followed by annotations.

<img src="imgs/df.png" alt="Dataframe" width="400">

Then it just replaces values from this file into the templates defined in itol_text.py.

It will generate a colour_dict automatically, but you can also just define your own colours and pass in a colour_dict (there's a comment in the code where you can override it).

It generates these three styles of annotations:

Colour ranges (from 'xref_orthodb' column)

<img src="imgs/ranges.png" alt="Ranges" width="400">

Colour strips (from lineage_superkingdom, lineage_phylum)

<img src="imgs/colour_strips.png" alt="Colour Strips" width="400">

Text on extants / ancestors (from value column)

<img src="imgs/text.png" alt="Text" width="400">

# Note for ranges

Note that for ranges you need to toggle - 'Cover leaf labels' and 'Extend to fit labels' to view them correctly

<img src="imgs/itol_options.png" alt="iTOL Options" width="200">


