using System;
using System.Diagnostics;

namespace KnightsTour
{
    /*
    Searches for a solution for the Knight's Tour problem on a board of size n x n from a randomly generated
    starting point, using backtracking and Warnsdorff's algorithm.

    Created by Hannah Smith (student number 216019732) with reference to code available at:
    https://kalkicode.com/warnsdorffs-algorithm-knights-tour-problem
    */
    public class Solution
    {
        //-- Instance variables --//
        private Board _board;
        // Tracks the current square in the board during the search.
        private (int, int) _current;
        // Records the starting point to check for a closed tour
        private (int, int) _start;
        // Helper arrays to represent possible moves by the knight chess piece.
        private static int[] _rowMove = { 2, 1, -1, -2, -2, -1, 1, 2 };
        private static int[] _colMove = { 1, 2, 2, 1, -1, -2, -2, -1 };

        //-- Methods --//
        public Solution()
        {
            /* Generates a new solution using the input n to create a board of size n x n */
            int n = GetStart();
            this._board = new Board(n);
        }

        public void FindValid()
        {
            /* Searches for a valid solution from a randomly generated starting point */

            ChooseStartSquare(this._board.BoardSize);
            Console.WriteLine("Starting from " + this._current.Item1.ToString() + ", " + this._current.Item2.ToString());

            Stopwatch timer = new Stopwatch(); // Used for time out and reporting program running time.
            timer.Start();
            while (true)
            {
                bool solved = Solve();
                if (solved)
                {
                    Console.WriteLine("(Total running time is {0})", timer.Elapsed);
                    break;
                }
                if (timer.ElapsedMilliseconds > 5000)
                {
                    PrintSolution(false);
                    throw new TimeoutException();
                }
            }
        }
        public void ChooseStartSquare(int n)
        {
            /* Chooses a random square on the board to start searching from. */
            var rand = new Random();
            (int, int) start = (rand.Next(n), rand.Next(n));
            this._start = start;
            this._current = start; // Sets the chosen square to the current search point.
            this._board.BoardArray[start.Item1, start.Item2] = 1; // Records the starting square's move number.
        }

        public int GetStart()
        {
            // Prompts the user for a chessboard size continually until an acceptable size is chosen
            int n;
            Start:
            Console.WriteLine("Please enter the size of the chess board: ");
            try
            {
                n = Convert.ToInt32(Console.ReadLine());
            }
            catch
            {
                Console.WriteLine("You have entered an incorect input format.");
                goto Start;
            }
            if (n < 5)
            {
                Console.WriteLine("Please enter a number greater than 4.");
                goto Start;
            }
            return n;
        }
        public static bool ValidMove(int[,] boardArray, int BoardSize, (int, int) move)
        {
            /* Returns true if the move is valid i.e. within the board space and to unvisited squares. */
            int rowmove = move.Item1, colmove = move.Item2;
            return (rowmove < BoardSize && rowmove >= 0 && colmove < BoardSize && colmove >= 0 && (boardArray[rowmove, colmove] < 0));
        }
        public bool Solve()
        {
            /* Provides a solution from the current point and returns true when a solution is found.*/
            int searchSpace = this._board.BoardSize * this._board.BoardSize; // Search space represents the number of squares on the board.
            for (int i = 0; i < searchSpace - 1; i++)
            {
                if (ChooseNextSquare() == false) { return false; }
            }
            PrintSolution(true); // Prints a solution to the console if one is found.
            return true;
        }
        public int CountNeighbours((int,int) square)
        {
            /* Counts the number of valid onward moves from a given square. */
            int neighbours = 0;
            for (int i = 0; i < 8; i++)
            {
                if (ValidMove(this._board.BoardArray, this._board.BoardSize, (square.Item1 + _rowMove[i], square.Item2 + _colMove[i])))
                {
                    neighbours++;
                }
            }
            return neighbours;
        }
        private bool ChooseNextSquare()
        {
            /* Chooses the square with the minimum onward moves to move to.
            If no valid onward moves are found, returns false.
            Otherwise this method implements the move to the next square and returns true. */
            (int, int) next;
            (int, int) current = this._current;
            Random rand = new Random();
            int start = rand.Next(0, 8); // Chooses at random from the possible 8 moves a knight can take to start searching from.
            int min = 9;
            int nextIndex = -1, index = -1;
            int neighboursCount;

            // Searching for the neighbour with the fewest onward moves.
            for (int i = 0; i < 8; i++)
            {
                index = (start + i) % 8;
                next = (current.Item1 + _rowMove[index], current.Item2 + _colMove[index]);
                if (ValidMove(_board.BoardArray, _board.BoardSize, next))
                {
                    neighboursCount = CountNeighbours(next);
                    if (neighboursCount < min)
                    {
                        nextIndex = index;
                        min = neighboursCount;
                    }
                }
            }

            if (min == 9) { return false; } // If the min does not go below 9, there are no possible onward moves.

            // Implementing the next move
            next = (current.Item1 + _rowMove[nextIndex], current.Item2 + _colMove[nextIndex]);
            this._board.BoardArray[next.Item1, next.Item2] = this._board.BoardArray[current.Item1, current.Item2] + 1;
            this._current = next;
            return true;
        }

        private void PrintSolution(bool foundValid)
        {
            /* Prints the board according to whether a valid solution was found.*/
            if (foundValid)
            {
                Console.WriteLine("Final Game Board: ");
                this._board.DrawBoard(true); // Valid solutions print the move order.
            }
            else
            {
                Console.WriteLine("No solutions from this starting point: ");
                this._board.DrawBoard(false); // Invalid paths are just printed by which squares were visited or not.
            }
        }

        //-- Properties --//
        public Board SolutionBoard
        {
            get { return _board; }
        }

        public class Board
        {
            //-- Instance variables --//
            private int[,] _boardArray;
            private int _boardSize;

            //-- Methods --//
            public Board(int n)
            {
                /* Generating a new board of length n x n.*/
                this._boardArray = new int[n,n];
                this._boardSize = n;
                PopulateBoard(this._boardArray, n);
            }
            private void PopulateBoard(int[,] array, int n)
            {
                /* Populates a new board with univisited squares, as represented by a negative move number. */
                for (int i = 0; i < n; i++)
                {
                    for (int j = 0; j < n; j++)
                    {
                        array[i,j] = -1;
                    }
                }
            }
            public void DrawBoard(bool verbose)
            {
                /* Displays the game board to the console. */
                for (int i = 0; i < this._boardSize; i++)
                {
                    for (int j = 0; j < this._boardSize; j++)
                    {
                        if (this._boardArray[i,j] != -1)
                        {
                            if (verbose) // If verbose the game board will display as the move numbers.
                            {
                                Console.Write(this._boardArray[i,j].ToString() + "\t");
                            }
                            else { Console.Write('X' + "\t"); } // If not verbose the game board will show the visited versus the unvisited squares on the board.
                        }
                        if (this._boardArray[i,j] == -1)
                        {
                            Console.Write('-' + "\t");
                        }
                    }
                    Console.Write("\n");
                }
            }

            //-- Properties --//
            public int[,] BoardArray
            {
                get { return _boardArray; }
                set { _boardArray = value; }
            }
            public int BoardSize{ get { return _boardSize; }}
        }
        static void Main(string[] args)
        {
            Solution tester = new Solution();
            tester.FindValid();
        }
    }
}