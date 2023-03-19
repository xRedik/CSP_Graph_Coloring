# CSP Graph Coloring (Farid Guliyev)

The program was written with the command line interfaces. That is why we should run this program with several flags. Here is the table of flags:

| Flag  | Purpose | Requred or not | Default value |
| ------------- | ------------- | ------------- | ------------- |
| -f FILENAME, --filename FILENAME  | name of the input file  | Required  | No default value  |
| -g, --gui, --no-gui  | display GUI  | Not required | –gui |
| -a, --auto, --no-auto | automatic or manual coloring | Not required | –auto | 
| -t, --run_test, --no-run_test | flag for running the test | Not required | –run_test | 

The program also has the -h flag to show the help message to the user about usage of flags. It was included by the argparse package itself.

The main purpose of the –auto flag is just for visualization purposes. If our program runs with auto mode, all the vertices will be shown as colored in the GUI. However, if we run the program with manual mode (--no-auto) the vertices will be displayed with default black color, and using the right key, the vertices will be colored one by one for each right key press. However, if we press the left key, the last vertex will come back to the default color which is black.

Here is the example of running the program with a command line interface. <br>
``` python .\main.py -f .\input_files\input_text_3.txt -g -a -t ``` <br> <br>
The ouput of the program will be like that <br>
![auto mode](https://user-images.githubusercontent.com/56725845/226175771-d3996de6-eafb-4321-bf43-30c9cae23fe7.gif)

However, if we run our program with manual mode or no-auto mode, the command line would be like that: <br>
``` python .\main.py -f .\input_files\input_text_3.txt -g --no-auto -t ``` <br> <br>
And output of the program would be like that: <br>
![manual mode](https://user-images.githubusercontent.com/56725845/226175828-109cf5eb-9ef1-4aec-9dd2-9796d73bfd37.gif)

As you can see in the manual mode, I go back and forward for coloring the vertex. However, all the algorithm of CSP are same for the both cases. It is just for visualization purposes.

