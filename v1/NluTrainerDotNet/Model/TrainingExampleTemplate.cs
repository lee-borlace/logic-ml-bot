using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace NluTrainerDotNet.Model
{
    public class TrainingExampleTemplate
    {
        public string Id { get; set; }

        public string ExampleText { get; set; }

        public string Language { get; set; }

        public string Logic { get; set; }

        /// <summary>
        /// E.g. Statement, Question, Command, Social, Unknown
        /// </summary>
        public string SentenceType { get; set; }

        public Visibility ExampleTextVisibility
        {
            get
            {
                return string.IsNullOrWhiteSpace(ExampleText) ? Visibility.Collapsed : Visibility.Visible;
            }
        }

        public Visibility LanguageVisibility
        {
            get
            {
                return string.IsNullOrWhiteSpace(Language) ? Visibility.Collapsed : Visibility.Visible;
            }
        }

        public Visibility LogicVisibility
        {
            get
            {
                return string.IsNullOrWhiteSpace(Logic) ? Visibility.Collapsed : Visibility.Visible;
            }
        }
    }
}
