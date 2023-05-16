namespace SpreadsheetEngine
{
    internal class VNode : Node
    {
        public VNode(string name, double value)
            : base(value.ToString())
        {
            this.Name = name;
            this.Value = value;
        }

        public string Name { get; set; }

        public double Value { get; set; }
    }
}
