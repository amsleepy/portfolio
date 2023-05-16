namespace Spreadsheet_Tests
{
    using SpreadsheetEngine;

    public class ExpressionTreeTests
    {
        [Test]
        public void Test1()
        {
            ExpressionTree exp = new ExpressionTree("1+2+3+4");
            Assert.That(exp.Evaluate(), Is.EqualTo(10.0));
        }

        [Test]
        public void Test2()
        {
            ExpressionTree exp = new ExpressionTree("Arizona-2+((4/2))");
            exp.SetVariable("Arizona", 12.5);

            Assert.That(exp.Evaluate(), Is.EqualTo(12.5));
        }

        [Test]
        public void Test4()
        {
            ExpressionTree exp = new ExpressionTree("24/2*6+2");
            Assert.That(exp.Evaluate(), Is.EqualTo(74));
        }

        [Test]
        public void Test5()
        {
            ExpressionTree exp = new ExpressionTree("24/2*6+2");
            Assert.That(exp.PostOrder, Is.EqualTo("24 2 / 6 * 2 + "));
        }

        [Test]
        public void Test6()
        {
            ExpressionTree exp = new ExpressionTree("2");
            Assert.That(exp.Evaluate, Is.EqualTo(2));
        }
    }
}
