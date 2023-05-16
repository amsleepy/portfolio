namespace SpreadsheetEngine
{
    using System.Linq;

    internal class SubtractionOp : ONode
    {
        public SubtractionOp()
            : base('-')
        {
            this.priority = 1;
            this.associativity = 0;
        }

        public override double EvalOperation()
        {
            if (this.Left is ONode && this.Right is ONode)
            {
                ONode left = (ONode)this.Left;
                ONode right = (ONode)this.Right;

                return left.EvalOperation() - right.EvalOperation();
            }
            else if (this.Left is ONode)
            {
                ONode left = (ONode)this.Left;

                return left.EvalOperation() - double.Parse(this.Right.value);
            }
            else if (this.Right is ONode)
            {
                ONode right = (ONode)this.Right;

                return double.Parse(this.Left.value) - right.EvalOperation();
            }
            else
            {
                return double.Parse(this.Left.value) - double.Parse(this.Right.value);
            }
        }
    }
}
