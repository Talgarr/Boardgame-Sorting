# Board game Sorting
Boardgame sorting algorithm to fit your collection perfectly in an organizer respecting a given parameter.
The intended use was to sort a boardgame collection vertically in an IKEA Kallax by weight with every cube fitting perfectly.

## Getting started
1. Create a *.csv* (with Excel, Calc or others) with the name of your board games in the first column, the given parameter in the second column and the length of the game in the third column. See *template.csv* for a template.
  
&emsp;&emsp;**Note**: the decimal marker must be a dot. The first row of the file is ignored.

2. Comments out with **~**  

3. Change the variables at the top of *main.py* according to your setup. 

&emsp;&emsp;a. WIDTH: This should be the space you have in your organizer. The default is 336mm which is a standard Kallax.
  
&emsp;&emsp;b. WIDTH_TOLERANCE_MIN, WIDTH_TOLERANCE_MAX: The minimum and maximum space left in a cube. By experience, 1-2mm is perfect, but it heavily depends on the way you took your measurements.
  
&emsp;&emsp;c. MAX_PARAM_TOLERANCE: Will determine how far at the maximum to look in the collection to fit the games. If no valid combination is found, try using a higher number.
  
&emsp;&emsp;d. PATH_TO_COLLECTION: Path to your *.csv* file.
  
4. Run and enjoy! The program output the result in *result.txt*.

## BoardGameGeek
I also included a way to transfer your BGG collection directly to this software format. You'll need to add the length to your comments or private comments.

1. Download your collection from BGG, and select "all".

2. Change the parameters of *bgg2collection.py*:

&emsp;&emsp;a. PARAM: The evaluated parameter column in bgg.

&emsp;&emsp;a. LENGTH_COLUMN: *comment* or *privatecomment*

&emsp;&emsp;a. LENGTH_NAME: What you used to mark the length in bgg.

&emsp;&emsp;a. path: Path to the collection downloaded from bgg.
