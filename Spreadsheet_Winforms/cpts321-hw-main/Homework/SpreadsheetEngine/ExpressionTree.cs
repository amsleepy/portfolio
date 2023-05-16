// Code by Stephen Emmons 11675051

namespace SpreadsheetEngine
{
    public class ExpressionTree
    {
        public Stack<Node> tree = new Stack<Node>();
        public Dictionary<string, double> Variables = new Dictionary<string, double>();
        private Stack<char> stack = new Stack<char>();
        private string postOrder = string.Empty;
        private ONodeFactory factory = new ONodeFactory();
        private Dictionary<char, Type> operators = new Dictionary<char, Type>();

        public ExpressionTree(string exp)
        {
            this.operators = this.factory.operators;
            this.postOrder = this.ParseExpression(exp);
        }

        public string PostOrder { get => this.postOrder; }

        public void SetVariable(string name, double value)
        {
            this.Variables[name] = value;
        }

        public string ParseExpression(string a) // a is the string/substring the tree recurses through
        {

            if (double.TryParse(a, out double value))
            {
                return value.ToString();
            }

            string postExpression = string.Empty;

            // Use Shunting Algorithm to build stack
            for (int i = 0; i < a.Length; i++)
            {
                // if char is an operator
                if (this.operators.ContainsKey(a[i]))
                {
                    // if stack is not empty
                    if (this.stack.TryPeek(out char c))
                    {
                        if (c == '(')
                        {
                            this.stack.Push(a[i]);
                        }

                        // if operator has greater precedence than operator on stack
                        else if (this.operators.ContainsKey(c))
                        {
                            ONode x = (ONode)Activator.CreateInstance(this.operators[a[i]]);
                            ONode y = (ONode)Activator.CreateInstance(this.operators[c]);

                            if (x.priority > y.priority)
                            {
                                this.stack.Push(a[i]);
                            }
                            else if (x.priority <= y.priority)
                            {
                                postExpression = postExpression + this.stack.Pop() + ' ';
                                i -= 1;
                            }
                        }
                    }

                    // stack is empty, push operator
                    else
                    {
                        this.stack.Push(a[i]);
                    }
                }
                else if (a[i] == '(')
                {
                    this.stack.Push(a[i]);
                }
                else if (a[i] == ')')
                {
                    // pop until left parentheses is spotted
                    char pop = this.stack.Pop();
                    while (pop != '(')
                    {
                        postExpression = postExpression + pop + ' ';
                        pop = this.stack.Pop();
                    }
                }

                // char is part of a variable or number, add to expression, don't bother with stack
                else if (a[i] != ' ')
                {
                    int start = i;
                    if (a.Length == 1)
                    {
                        postExpression = a;
                    }
                    else if (i == a.Length - 1 && !char.IsLetter(a[i - 1]) && !char.IsDigit(a[i - 1]))
                    {
                        postExpression = postExpression + a[i] + ' ';
                    }
                    else if (i != a.Length - 1)
                    {
                        // move pointer until the end of the variable or constant is found, increment after its found for use in substring method
                        while (a[i] != '(' && a[i] != ')' && !this.operators.ContainsKey(a[i]) && i < a.Length)
                        {
                            if (i == a.Length - 1)
                            {
                                i++;
                                break;
                            }

                            i++;
                        }

                        string sub = a.Substring(start, i - start);
                        postExpression = postExpression + sub + ' ';

                        i--;
                    }
                }
            }

            // pop everything on stack after full expression is read
            while (this.stack.TryPeek(out char c))
            {
                postExpression = postExpression + this.stack.Pop() + ' ';
            }

            return postExpression;
        }

        private void BuildTree(string post)
        {
            // operands are added to stack first, pop two when an operator is spotted and create sub tree and add it to the stack
            for (int i = 0; i < post.Length; i++)
            {
                if (post[i] == ' ')
                {
                }
                else if (this.operators.ContainsKey(post[i]))
                {
                    ONode operate = this.factory.CreateOperatorNode(post[i]);
                    operate.Right = this.tree.Pop();
                    operate.Left = this.tree.Pop();
                    this.tree.Push(operate);
                }
                else
                {
                    int start = i;
                    while (post[i] != ' ')
                    {
                        if (i == post.Length - 1)
                        {
                            break;
                        }

                        i++;
                    }

                    string sub = post.Substring(start, i - start);

                    if (double.TryParse(sub, out double d))
                    {
                        CNode constant = new CNode(d);
                        this.tree.Push(constant);
                    }
                    else
                    {
                        // catch when unassigned variable is used
                        try
                        {
                            VNode variable = new VNode(sub, this.Variables[sub]);
                            this.tree.Push(variable);
                        }
                        catch (Exception)
                        {
                            Console.WriteLine("Error: No value assigned to " + sub);
                            break;
                        }
                    }
                }
            }
        }

        public double? Evaluate()
        {
            double EvalHelp(Node node)
            {
                ONode on = (ONode)node;

                return on.EvalOperation();
            }

            if (double.TryParse(this.postOrder, out double x))
            {
                return x;
            }

            if (this.Variables.ContainsKey(this.postOrder.Substring(0, this.postOrder.Length - 1)))
            {
                return this.Variables[this.postOrder.Substring(0, this.postOrder.Length - 1)];
            }

            this.BuildTree(this.postOrder);
            ONode root;

            // will not try and evaluate if there is no operator in the expression
            try
            {
                root = (ONode)this.tree.Pop();
                return EvalHelp(root);
            }
            catch (Exception)
            {
                Console.WriteLine("Incorrect Expresion Format");
                return null;
            }
        }
    }
}
