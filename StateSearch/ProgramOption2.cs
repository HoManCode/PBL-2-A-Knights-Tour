using System;
using System.Diagnostics;

namespace KnightsTour
{
    namespace knightTour
    {
        class knightTour
        {
            //Represent the Knight's next move
            //x = x coordinate
            //y= y coordinate 
            static int[] xMove = { 2, 1, -1, -2, -2, -1, 1, 2 };
            static int[] yMove = { 1, 2, 2, 1, -1, -2, -2, -1 };

            //Declare variables
            static int board_size;
            static int row;
            static int column;

            //Ensures move occuring is valid ******************CHECKED
            static bool moveValidation(int[,] board, int row, int column)
            {
               
                return (row < board_size && row >= 0 && column < board_size && column >= 0 && board[row, column] == -1);
            }

            //Prints the resultant board to the console ******* CHECKED
            static void printBoard(int[,] board)
            {
                for (int i = 0; i < board_size; i++)
                {
                    for (int j = 0; j < board_size; j++)
                    {
                        Console.Write(board[i, j] + " ");
                    }
                    Console.WriteLine();
                }
            }

            static bool solveKnight()
            {
                //Creates an array from the user's indicated board size 
                int[,] board = new int[board_size, board_size];
              

                //Initiliazation of solution Matrix
                for (int i = 0; i < board_size; i++)
                {
                    for (int j = 0; j < board_size; j++)
                    {
                        board[i, j] = -1;
                    }
                }
                //Allows us to calculate runtime
                Stopwatch watch = new Stopwatch();
                watch.Start();

                //Knight begins at the first block
                board[0, 0] = 0;

                if (!solve(board, 0, 0, 1, xMove, yMove))
                {
                    Console.WriteLine("Solution does "
                              + "not exist");
                    return false;
                }
                else
                    Console.WriteLine("(Total running time is {0})", watch.Elapsed);
                printBoard(board);
                return true;
            }

            //Recursive utility function to solve KT
            static bool solve(int[,] board, int row, int column, int move, int[] xMove, int[] yMove)
            {
             
                if (move == board_size * board_size) return true;

                //Try all next moves from the current coordinates
                for (int i = 0; i < 8; i++)
                {
                    int new_x = row + xMove[i];
                    int new_y = column + yMove[i];
                    if (moveValidation(board, new_x, new_y))
                    {
                        board[new_x, new_y] = move;
                        if (solve(board, new_x, new_y, move + 1, xMove, yMove)) return true;
                        else board[new_x, new_y] = -1;
                    }
                }
                return false;
            }



            static void Main(String[] args)
            {
     
                //Prompts the user for a chessboard size continually until an acceptable size is chosen 
                Start:
                Console.WriteLine("Please enter the size of the chess board: ");
                try
                {
                    board_size = Int32.Parse(Console.ReadLine());
                }
                catch
                {
                    Console.WriteLine("You have entered an incorrect input format");
                    goto Start;
                }
                
                //Prompts the user for the Knight's current position continually until an acceptable position is chosen
                CoordinateValidation:
                try
                {
                    Console.WriteLine("Please enter the Knight's next move: ");
                    Console.WriteLine("x: ");
                     row = Int32.Parse(Console.ReadLine());
                    Console.WriteLine("y: ");
                    column = Int32.Parse(Console.ReadLine());
                }
                catch
                {
                    Console.WriteLine("You have entered an incorrect input format");
                    goto CoordinateValidation;
                }
                //Calls the knight tour solving methods
                solveKnight();
    
            
            }

        }
    }
}