using System;

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

            static void Main(String[] args)
            {
                int board_size;
                int row;
                int column;

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
                    Console.WriteLine("Please enter the current position of the knight: ");
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
              
                
                //Creates an array from the user's indicated board size 
                int[,] board = new int[board_size, board_size];
                int move = 0;

                for (int i = 0; i < board_size; i++)
                {
                    for (int j = 0; j < board_size; j++)
                    {
                        board[i, j] = 0;
                    }
                }

                solve(board, row, column, move);
                printBoard(board);
            }
            //Ensures move occuring is valid 
            static bool moveValidation(int[,] board, int row, int column)
            {
                int board_size = board.GetLength(0);
                return (row < board_size && row >= 0 && column < board_size && column >= 0 && board[row, column] == 0);
            }
            
            //Recursive utility function to solve KT
            static bool solve(int[,] board, int row, int column, int move)
            {
                int board_size = board.GetLength(0);
                if (move == board_size * board_size) return true;
                for (int i = 0; i < board_size; i++)
                {
                    int new_x = row + xMove[i];
                    int new_y = column + yMove[i];
                    if (moveValidation(board, new_x, new_y))
                    {
                        board[new_x, new_y] = move;
                        if (solve(board, new_x, new_y, move + 1)) return true;
                        else board[new_x, new_y] = 0;
                    }
                }
                return false;
            }

            //Prints the resultant board to the console
            static void printBoard(int[,] board)
            {
                for (int i = 0; i < board.GetLength(0); i++)
                {
                    for (int j = 0; j < board.GetLength(0); j++)
                    {
                        Console.Write(board[i, j] + " ");
                    }
                    Console.WriteLine();
                }
            }
        }
    }
}