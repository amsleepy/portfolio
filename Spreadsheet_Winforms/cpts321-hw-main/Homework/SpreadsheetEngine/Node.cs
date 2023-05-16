using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SpreadsheetEngine
{
    public abstract class Node
    {
        public string value;

        public Node(string v)
        {
            this.value = v;
        }
    }
}
