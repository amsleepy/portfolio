namespace SpreadsheetEngine
{
    internal abstract class ONode : Node
    {
        public int priority;
        public int associativity; // 0 for left, 1 for right, not using boolean because it breaks and idk why

        public ONode(char v)
            : base(v.ToString())
        {
            this.Op = (char)this.value[0];
            this.Left = this.Right = null;
        }

        public char Op { get; set; }

        public Node? Left { get; set; }

        public Node? Right { get; set; }

        public abstract double EvalOperation();

    }
}
