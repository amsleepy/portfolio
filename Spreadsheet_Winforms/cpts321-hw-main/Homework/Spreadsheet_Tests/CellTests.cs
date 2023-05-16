namespace Spreadsheet_Tests
{
    using SpreadsheetEngine;

    public class CellTests
    {
        [SetUp]
        public void Setup()
        {
        }

        [Test]
        public void Test1()
        {
            Spreadsheet spreadsheet = new Spreadsheet(26, 50); // testing that it doesn't crash
            Cell volcel = spreadsheet.GetCell(0, 0);
            Assert.Pass();
        }

        [Test]
        public void Test2() // testing value assignment with SetValue method
        {
            Spreadsheet spreadsheet = new Spreadsheet(26, 50);
            ConcreteCell cell = new ConcreteCell(0, 0);

            Cell val = spreadsheet.GetCell(1, 2);
            cell.SetValue(val.Value);

            Assert.That(val.Value, Is.EqualTo(cell.Value));
        }

        [Test]
        public void Test3() // testing value assignment with text setter
        {
            Spreadsheet spreadsheet = new Spreadsheet(26, 50);
            Cell volcel = spreadsheet.GetCell(0, 0);
            volcel.Text = "Testing...";
            Assert.That("Testing...", Is.EqualTo(volcel.Text));
        }

        [Test]
        public void Test4() // testing logic for expression case in CellPropertyChanged
        {
            Spreadsheet spreadsheet = new Spreadsheet(26, 50);
            ConcreteCell cell = new ConcreteCell(0, 0);

            cell.Text = "=12";
            char column = cell.Text[1]; // assume cellname in formula is cell dimensions with no characters in between
            char row = cell.Text[2];

            int in1 = column - 0;
            int in2 = row - 0;

            Cell val = spreadsheet.GetCell(1, 2);
            cell.SetValue(val.Value);

            Assert.That(val.Value, Is.EqualTo(cell.Value));
        }

        [Test]
        public void Test5() // testing nonexistent reference
        {
            Spreadsheet spreadsheet = new Spreadsheet(26, 50);
            double? val = 0;

            ExpressionTree exp = new ExpressionTree("B2+4+(30/4)");
            val = exp.Evaluate();

            Cell cell = spreadsheet.GetCell(0, 0);
            cell.Text = "=B2+4+(30/4)";

            Assert.That(val, Is.EqualTo(null));
            Assert.That(cell.Value, Is.EqualTo("!(Bad Reference)"));
        }

        [Test]
        public void Test6() // testing self reference
        {
            Spreadsheet spreadsheet = new Spreadsheet(26, 50);

            Cell cell = spreadsheet.GetCell(0, 0);
            cell.Text = "=A2+4+(30/4)";
            Assert.That(cell.Value, Is.EqualTo("!(Bad Reference)"));
        }

        [Test]
        public void Test7() // testing circular reference
        {
            Spreadsheet spreadsheet = new Spreadsheet(26, 50);

            Cell cell1 = spreadsheet.GetCell(0, 0);
            cell1.Text = "=A2+4+(30/4)";

            Cell cell2 = spreadsheet.GetCell(0, 1);
            cell2.Text = "=A3+4+(30/4)";

            Cell cell3 = spreadsheet.GetCell(0, 2);
            cell3.Text = "=A4+4+(30/4)";

            Cell cell4 = spreadsheet.GetCell(0, 3);
            cell4.Text = "=A1+4+(30/4)";

            Assert.That(cell1.Value, Is.EqualTo("!(Bad Reference)"));
            Assert.That(cell2.Value, Is.EqualTo("!(Bad Reference)"));
            Assert.That(cell3.Value, Is.EqualTo("!(Bad Reference)"));
            Assert.That(cell4.Value, Is.EqualTo("!(Bad Reference)"));
        }
    }

    internal class ConcreteCell : Cell // instantiation of Cell to allow Spreadsheet to set values
    {
        public ConcreteCell(int colIn, int rowIn)
        {
            this.RowIndex = rowIn;
            this.ColumnIndex = colIn;
        }

        public void SetValue(string text)
        {
            this.value = text;
        }
    }
}