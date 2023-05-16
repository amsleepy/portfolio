// Code by Stephen Emmons 11675051

namespace SpreadsheetEngine
{
    using System.ComponentModel;
    using System.Xml;
    using System.Xml.Linq;

    public class Spreadsheet : INotifyPropertyChanged
    {
        public string letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

        // spreadsheet will get variables from the UI and pass them to the expression tree
        public Dictionary<string, double> Variables = new Dictionary<string, double>();
        public Dictionary<Cell, List<Cell>> references = new Dictionary<Cell, List<Cell>>();

        private ConcreteCell[,] dimensions; // holds all the cells in the sheet (within cells interlinked, within cells interlinked)

        public Spreadsheet(int colNum, int rowNum)
        {
            this.dimensions = new ConcreteCell[colNum, rowNum];
            this.ColumnCount = colNum;
            this.RowCount = rowNum;

            // create empty cell for each spot in spreadsheet
            for (int i = 0; i < colNum; i++)
            {
                for (int j = 0; j < rowNum; j++)
                {
                    ConcreteCell newCell = new ConcreteCell(i, j);
                    newCell.PropertyChanged += this.CellPropertyChangedHandler;
                    this.dimensions[i, j] = newCell;
                }
            }
        }

        public event PropertyChangedEventHandler? PropertyChanged;

        public int ColumnCount { get; }

        public int RowCount { get; }

        public Cell? GetCell(int colIn, int rowIn)
        {
            if (this.dimensions[colIn, rowIn] != null)
            {
                return this.dimensions[colIn, rowIn];
            }

            return null;
        }

        public void SetCell(Cell cell, string text)
        {
            ConcreteCell c = (ConcreteCell)cell;
            c.SetValue(text);
        }

        public void CellColorUpdate(uint color, int col, int row)
        {
            this.dimensions[col, row].BG = color;
        }

        public void Save(StreamWriter sr)
        {
            XmlDocument doc = new XmlDocument();
            XmlElement root = doc.CreateElement("Spreadsheet");
            doc.AppendChild(root);

            foreach (Cell cell in this.dimensions)
            {
                // if cell has been edited, add it to xml file
                if (cell.Text != null || cell.BG != 0xFFFFFF)
                {
                    XmlElement child = doc.CreateElement("Cell");
                    child.SetAttribute("Name", letters[cell.ColumnIndex] + cell.RowIndex.ToString());

                    XmlElement text = doc.CreateElement("Text");
                    text.InnerText = cell.Text;

                    XmlElement bg = doc.CreateElement("BGColor");
                    bg.InnerText = cell.BG.ToString();

                    child.AppendChild(text);
                    child.AppendChild(bg);
                    root.AppendChild(child);
                }
            }

            doc.Save(sr);
            sr.Close();
        }

        public void Load(StreamReader sr)
        {
            XDocument doc = XDocument.Load(sr);

            // check if each cell is in the xml file, if it is, update
            foreach (Cell cell in this.dimensions)
            {
                foreach (var child in doc.Root.Elements("Cell"))
                {
                    XAttribute a = child.Attribute("Name");
                    string val = a.Value;

                    if (val == letters[cell.ColumnIndex] + cell.RowIndex.ToString())
                    {
                        if (child.Element("Text").Value != null)
                        {
                            cell.Text = child.Element("Text").Value;
                        }

                        cell.BG = uint.Parse(child.Element("BGColor").Value);
                    }
                }
            }

            sr.Close();
        }

        public List<Cell> UpdateCells(List<Cell> cells)
        {
            List<Cell> originalCells = new List<Cell>();

            foreach (Cell cell in cells)
            {
                originalCells.Add(this.GetCell(cell.ColumnIndex, cell.RowIndex).Clone());

                this.GetCell(cell.ColumnIndex, cell.RowIndex).Text = cell.Text;
                this.GetCell(cell.ColumnIndex, cell.RowIndex).BG = cell.BG;
            }

            return originalCells;
        }

        private void CellPropertyChangedHandler(object? sender, PropertyChangedEventArgs e) // event handler to be passed to UI
        {
            ConcreteCell cell = (ConcreteCell)sender;

            if (e.PropertyName != "BG")
            {
                if (cell.Text != null && cell.Text != "")
                {
                    if (cell.Text[0] != '=')
                    {
                        ((ConcreteCell)sender).SetValue(cell.Text);
                        string colVar = letters[cell.ColumnIndex] + (cell.RowIndex + 1).ToString();

                        // Remove from variables if cell no longer has a numeric value/add variable if it does
                        if (double.TryParse(cell.Value, out double dub))
                        {
                            if (this.Variables.ContainsKey(colVar))
                            {
                                this.Variables.Remove(colVar);
                            }
                            else
                            {
                                this.Variables[colVar] = dub;
                            }
                        }
                        else if (this.Variables.ContainsKey(colVar))
                        {
                            this.Variables.Remove(colVar);
                        }
                    }
                    else
                    {
                        string expression = cell.Text.Substring(1, cell.Text.Length - 1);
                        ExpressionTree exp = new ExpressionTree(expression);
                        exp.Variables = this.Variables;
                        double? eval = exp.Evaluate();
                        string colVar = letters[cell.ColumnIndex] + (cell.RowIndex + 1).ToString();


                        if (eval != null)
                        {
                            ((ConcreteCell)sender).SetValue(eval.ToString());
                        }
                        else
                        {
                            ((ConcreteCell)sender).SetValue("!(Bad Reference)");

                            if (this.Variables.ContainsKey(colVar))
                            {
                                this.Variables.Remove(colVar);
                            }
                        }

                        // check if value is an expression and update variables dictionary if it is
                        if (this.Variables.ContainsKey(colVar) && double.TryParse(cell.Value, out double d))
                        {
                            this.Variables[colVar] = d;
                        }

                        // update cells that reference cell
                        if (this.references.ContainsKey(cell))
                        {
                            foreach (Cell c in this.references[cell])
                            {
                                Cell spreadCell = this.GetCell(c.ColumnIndex, c.RowIndex);
                                spreadCell.NotifyPropertyChanged();
                            }
                        }

                        // adds each cell in formula to references to make sure it updates when those cells are updated
                        if (double.TryParse(cell.Value, out double dub) && cell.Text != null)
                        {
                            this.Variables[colVar] = dub;

                            // check if cell text contains variables
                            if (cell.Text.Any(x => char.IsLetter(x)))
                            {
                                List<string> foundVars = new List<string>();

                                // find variables in text
                                for (int i = 0; i < cell.Text.Length; i++)
                                {
                                    if (char.IsLetter(cell.Text[i]))
                                    {
                                        try
                                        {
                                            foundVars.Add(cell.Text[i].ToString() + cell.Text[i + 1].ToString());
                                        }
                                        catch (Exception)
                                        {
                                            Console.WriteLine("Error: Variable in incorrect format");
                                            break;
                                        }
                                    }
                                }

                                try
                                {
                                    // add/updated referenced variables in reference dictionary
                                    foreach (string var in foundVars)
                                    {
                                        int row = int.Parse(var[1].ToString()) - 1;
                                        int col = letters.IndexOf(var[0]);
                                        Cell currCell = this.GetCell(col, row);

                                        if (!this.references.ContainsKey(currCell))
                                        {
                                            this.references.Add(currCell, new List<Cell>());
                                            this.references[currCell].Add(cell);
                                        }
                                        else
                                        {
                                            if (!this.references[currCell].Contains(cell))
                                            {
                                                this.references[currCell].Add(cell);
                                            }
                                        }
                                    }
                                }
                                catch (Exception)
                                {
                                    Console.WriteLine("Error: One or more variables in expression have no value");
                                }
                            }
                        }
                    }
                }
            }

            PropertyChangedEventHandler? handler = this.PropertyChanged;
            if (handler != null)
            {
                handler(this, new PropertyChangedEventArgs(cell.ColumnIndex.ToString() + (cell.RowIndex).ToString() + e.PropertyName[0]));
            }
        }

        internal class ConcreteCell : Cell // instantiation of Cell to allow Spreadsheet to set values
        {
            public ConcreteCell()
            {
            }

            public ConcreteCell(int colIn, int rowIn)
            {
                this.RowIndex = rowIn;
                this.ColumnIndex = colIn;
            }

            public void SetValue(string text) // access protected member, can only be called by Spreadsheet
            {
                this.value = text;
            }
        }
    }
}
