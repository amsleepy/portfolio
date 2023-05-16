// Code by Stephen Emmons 1167051

namespace SpreadsheetEngine
{
    using System.ComponentModel;
    using System.Runtime.CompilerServices;
    using System.Xml;
    using System.Xml.Schema;
    using System.Xml.Serialization;

    public abstract class Cell : INotifyPropertyChanged
    {
        public static int writeCount = 0;
        protected string name;
        protected uint BGColor = 0xFFFFFF;
        protected string? text;
        protected string? value;

        public event PropertyChangedEventHandler? PropertyChanged;

        public int RowIndex { get; set; }

        public int ColumnIndex { get; set; }

        public string Text
        {
            get => this.text;
            set
            {
                this.text = value;
                this.NotifyPropertyChanged("Text");
            }
        }

        public uint BG
        {
            get => this.BGColor;
            set
            {
                if (this.BGColor != value)
                {
                    this.BGColor = value;
                    this.NotifyPropertyChanged("BG");
                }
            }
        }

        public string Value { get => this.value; } // readonly

        public void NotifyPropertyChanged([CallerMemberName] string? propertyName = null)
        {
            PropertyChangedEventHandler? handler = this.PropertyChanged;
            if (handler != null)
            {
                handler(this, new PropertyChangedEventArgs(propertyName));
            }
        }

        public Cell Clone()
        {
            return (Cell)this.MemberwiseClone();
        }
    }
}
