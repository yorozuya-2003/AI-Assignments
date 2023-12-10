# Assignment-1 (Sorting as Searching)

**Name:** Tanish Pagaria  
**Roll No.:** B21AI040

## Directory Structure

- ### `B21AI40_Assig1.ipynb`
  #### `hashfunc`

  A hash function to aid in checking if an array is present in an array of arrays.

  - **Input:** array
  - **Returns:** string (hashed input)

  #### `gen_states`

  A function to generate children states by swapping elements.

  - **Input:** array (state)
  - **Returns:** array of children arrays (states)

  #### `check_sorted`

  - **Input:** array
  - **Returns:** boolean indicating whether an array is sorted or not

  #### `cost`

  - **Input:** array (state)
  - **Returns:** cost of the edge of the state graph (1 for all edges in this case)

  #### `show_path`

  - **Input:** array (list of states)
  - Prints the path using the input list

  #### `make_start_state`

  - **Input:** number of elements required in a state (integer)
  - **Returns:** array containing n float values (up to 1 decimal place) in the range (-10, 10)

  #### `run_algo`

  - **Inputs:**
    - n (number of elements, for generating a random state),
    - no. of iterations,
    - optional (in case of giving your state)
  - **Returns:** a dictionary containing the sum of total nodes covered for each algorithm for all iterations

  #### `print_algo_results`

  - **Inputs:**
    - dictionary (from the `run_algo` function),
    - integer (number of elements in a state),
    - integer (number of iterations)
  - Prints the average number of nodes explored for each algorithm for the given number of iterations

  #### Algorithm Functions

  All other functions in the notebook implement or aid the algorithms taking the state array as input. They use a fringe depending on the algorithm and heuristic function in some cases, keep a visited array to check previously covered states to prevent repetition, and return an array of states in the path or final state (in the case of hill climbing search).

- ### `B21AI040_Assig2.pdf`
  Report for the assignment describing experimental details, results, observations, analyses, etc.
