namespace SpreadsheetEngine
{
    using System.Linq;
    using System.Reflection;

    internal class ONodeFactory
    {
        public Dictionary<char, Type> operators = new Dictionary<char, Type>();

        public ONodeFactory()
        {
            this.TraverseAvailableOperators((op, type) => this.operators.Add(op, type));
        }

        private delegate void OnOperator(char op, Type type);

        public ONode CreateOperatorNode(char op)
        {
            if (this.operators.ContainsKey(op))
            {
                object operatorNodeObject = System.Activator.CreateInstance(operators[op]);
                if (operatorNodeObject is ONode)
                {
                    return (ONode)operatorNodeObject;
                }
            }

            throw new Exception("Unhandled operator");
        }

        private void TraverseAvailableOperators(OnOperator onOperator)
        {
            Type operatorNodeType = typeof(ONode);

            foreach (var assembly in AppDomain.CurrentDomain.GetAssemblies())
            {
                IEnumerable<Type> operatorTypes = assembly.GetTypes().Where(type => type.IsSubclassOf(operatorNodeType));

                foreach (var type in operatorTypes)
                {
                    PropertyInfo operatorField = type.GetProperty("Op");
                    if (operatorField != null)
                    {
                        object value = operatorField.GetValue(Activator.CreateInstance(type));
                        if (value is char)
                        {
                            char operatorSymbol = (char)value;
                            onOperator(operatorSymbol, type);
                        }
                    }
                }
            }
        }
    }
}
