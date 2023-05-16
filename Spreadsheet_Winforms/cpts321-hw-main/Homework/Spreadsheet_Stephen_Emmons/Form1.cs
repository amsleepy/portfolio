// Code by Stephen Emmons 11675051

namespace Spreadsheet_Stephen_Emmons
{
    using System.Collections.Generic;
    using System.ComponentModel;
    using System.Drawing;
    using System.Linq;
    using System.Runtime.ConstrainedExecution;
    using SpreadsheetEngine;

    #pragma warning disable SA1601 // Partial elements should be documented
    public partial class Form1 : Form
    {
        private Spreadsheet spread = new Spreadsheet(26, 50);
        private Stack<List<Cell>> undo = new Stack<List<Cell>>();
        private Stack<List<Cell>> redo = new Stack<List<Cell>>();

        public Form1()
        {
            this.InitializeComponent();
            this.AddColumnsRows();
            this.spread.PropertyChanged += this.CellPropertyChangedEventHandler;
            this.ChangeCellColorMenu.Click += this.ChangeCellColorMenu_Click;
            this.Undo.Click += this.UndoClick;
            this.Redo.Click += this.RedoClick;
            this.dataGridView1.CellBeginEdit += this.DataGridView1_CellBeginEdit;
            this.dataGridView1.CellEndEdit += this.DataGridView1_CellEndEdit;
            this.editMenu.DropDownOpening += this.EditOpen;
            this.SaveMenu.Click += this.SaveClick;
            this.LoadMenu.Click += this.LoadClick;
            }

        public void AddColumnsRows()
        {
            this.dataGridView1.Columns.Clear();
            this.dataGridView1.Rows.Clear();

            for (char c = 'A'; c <= 'Z'; c++)
            {
                this.dataGridView1.Columns.Add(char.ToString(c), char.ToString(c));
            }

            for (int i = 1; i <= 50; i++)
            {
                int rowNum = this.dataGridView1.Rows.Add();
                DataGridViewRow row = this.dataGridView1.Rows[rowNum];
                row.HeaderCell.Value = i.ToString();
            }
        }

        private void CellPropertyChangedEventHandler(object sender, PropertyChangedEventArgs e)
        {
            // subscribed to spreadsheet object's cellpropertychanged event
            Cell cell = this.spread.GetCell(int.Parse(e.PropertyName[0].ToString()), int.Parse(e.PropertyName[1].ToString()));
            DataGridViewCell gridCell = this.dataGridView1.Rows[cell.RowIndex].Cells[cell.ColumnIndex];

            if (e.PropertyName[2] == 'T')
            {
                // change cell text
                gridCell.Value = cell.Value;
            }

            if (e.PropertyName[2] == 'B')
            {
                // update color
                gridCell.Style.BackColor = ColorTranslator.FromHtml(cell.BG.ToString());
            }
        }

        private void DataGridView1_CellBeginEdit(object sender, DataGridViewCellCancelEventArgs e)
        {
            DataGridViewCell gridCell = this.dataGridView1.Rows[e.RowIndex].Cells[e.ColumnIndex];
            gridCell.Value = this.spread.GetCell(e.ColumnIndex, e.RowIndex).Text;
        }

        private void DataGridView1_CellEndEdit(object sender, DataGridViewCellEventArgs e)
        {
            DataGridViewCell gridCell = this.dataGridView1.Rows[e.RowIndex].Cells[e.ColumnIndex];
            Cell clone = this.spread.GetCell(e.ColumnIndex, e.RowIndex).Clone();

            List<Cell> changedCell = new List<Cell>() { clone }; // stores clone of cell to be changed so it can be undone if needed

            if (gridCell.Value != null)
            {
                this.spread.GetCell(e.ColumnIndex, e.RowIndex).Text = gridCell.Value.ToString();
            }

            // only push to undo stack if cell actually changed
            if (this.spread.GetCell(e.ColumnIndex, e.RowIndex).Text != clone.Text)
            {
                this.undo.Push(changedCell);
            }
        }

        private void ChangeCellColorMenu_Click(object sender, EventArgs e)
        {
            int selectedCellCount = this.dataGridView1.GetCellCount(DataGridViewElementStates.Selected);
            DataGridViewSelectedCellCollection selected = this.dataGridView1.SelectedCells;

            if (selectedCellCount > 0)
            {
                ColorDialog cd = new ColorDialog();
                List<Cell> changedCells = new List<Cell>();

                if (cd.ShowDialog() == DialogResult.OK)
                {
                    for (int i = 0; i < selectedCellCount; i++)
                    {
                        int row = selected[i].RowIndex;
                        int col = selected[i].ColumnIndex;

                        changedCells.Add(this.spread.GetCell(col, row).Clone());

                        Color clr = cd.Color;

                        // convert Color to hex value and update cell's bg field
                        string c = ColorTranslator.ToHtml(Color.FromArgb(clr.ToArgb()));
                        c = "0x" + c.Substring(1, c.Length - 1);
                        this.spread.CellColorUpdate(Convert.ToUInt32(c, 16), col, row);
                    }
                }

                this.undo.Push(changedCells);
            }
        }

        private void UndoClick(object sender, EventArgs e)
        {
            List<Cell> undoedCells = this.undo.Pop();
            this.redo.Push(this.spread.UpdateCells(undoedCells));
        }

        private void RedoClick(object sender, EventArgs e)
        {
            List<Cell> redoedCells = this.redo.Pop();
            this.undo.Push(this.spread.UpdateCells(redoedCells));
        }

        private void EditOpen(object sender, EventArgs e)
        {
            if (!this.undo.TryPeek(out List<Cell> r))
            {
                this.Undo.Visible = false;
            }
            else
            {
                this.Undo.Visible = true;
            }

            if (!this.redo.TryPeek(out List<Cell> x))
            {
                this.Redo.Visible = false;
            }
            else
            {
                this.Redo.Visible = true;
            }
        }

        private void SaveClick(object sender, EventArgs e)
        {
            SaveFileDialog sd = new SaveFileDialog();
            sd.Title = "Save";
            sd.Filter = "XML File | *.xml";

            if (sd.ShowDialog() == DialogResult.OK)
            {
                this.spread.Save(new StreamWriter(sd.FileName));
            }

            sd.Dispose();
        }

        private void LoadClick(object sender, EventArgs e)
        {
            OpenFileDialog od = new OpenFileDialog();
            od.Title = "Load";
            od.Filter = "XML File | *.xml";

            if (od.ShowDialog() == DialogResult.OK)
            {
                this.undo.Clear();
                this.redo.Clear();
                this.dataGridView1.Rows.Clear();
                this.AddColumnsRows();
                this.spread.Load(new StreamReader(od.FileName));
            }

            od.Dispose();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
        }
    }
}