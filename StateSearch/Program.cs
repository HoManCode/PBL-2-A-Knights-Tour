
//https://www.geeksforgeeks.org/the-knights-tour-problem-backtracking-1/
namespace knightTour
{
    class knightTour
    {
        static int [] xMove = {2,1,-1,-2,-2,-1,1,2};
        static int [] yMove = {1,2,2,1,-1,-2,-2,-1};

        static void Main(String[] args)
        {
            Console.WriteLine("Please enter the size of the chess board: ");
            int board_size = Int32.Parse(Console.ReadLine());
            Console.WriteLine("Please enter the current position of the knight: ");
            Console.WriteLine("x: ");
            int row = Int32.Parse(Console.ReadLine());
            Console.WriteLine("y: ");
            int col = Int32.Parse(Console.ReadLine());
            
            int move = 0;
            int[,] board = new int [board_size,board_size];

            for(int i = 0; i < board_size;i++)
            {
                for (int j = 0; j < board_size; j++)
                {
                    board[i,j] = 0;
                }
            }
            
            solve(board, row, col, move);
            printBoard(board);
        }
        static bool moveValidation (int [,]board, int row, int col )
        {
            int board_size = board.GetLength(0);
            return (row < board_size && row >= 0 && col < board_size && col >=0 && board[row, col] == 0);
        }
        static bool solve(int[,]board, int row, int col, int move)
        {
            int board_size = board.GetLength(0);
            if (move == board_size*board_size) return true;
            for (int i = 0; i < board_size; i++)
            {
                int new_x = row + xMove[i];
                int new_y = col + yMove[i];
                if (moveValidation(board, new_x, new_y))
                {
                    board[new_x,new_y] = move;
                    if (solve(board, new_x, new_y, move+1)) return true;
                    else board[new_x, new_y] = 0;
                }
            }
            return false;
        }

        static void printBoard(int[,] board)
        {
            for (int i = 0; i < board.GetLength(0); i++)
            {
                for (int j = 0; j < board.GetLength(0); j++)
                {
                    Console.Write(board[i,j] + " ");
                }
                Console.WriteLine();
            }
        }
    }
}