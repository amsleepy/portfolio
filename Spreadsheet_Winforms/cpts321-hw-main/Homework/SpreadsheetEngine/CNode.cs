namespace SpreadsheetEngine
{
    internal class CNode : Node
    {
        public CNode(double v)
            : base(v.ToString())
        {
            this.Value = v;
        }

        public double Value { get; set; }
    }
}
