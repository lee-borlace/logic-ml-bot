using Newtonsoft.Json;
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
        /// Frequency this example should be generated. 1-10. 1 = not frequent, 10 = very frequent
        /// </summary>
        public int Frequency { get; set; }

        /// <summary>
        /// E.g. Statement, Question, Command, Social, Unknown
        /// </summary>
        public string SentenceType { get; set; }

        [JsonIgnore]
        public Visibility LanguageVisibility
        {
            get
            {
                return string.IsNullOrWhiteSpace(Language) ? Visibility.Collapsed : Visibility.Visible;
            }
        }

        [JsonIgnore]
        public Visibility LogicVisibility
        {
            get
            {
                return string.IsNullOrWhiteSpace(Logic) ? Visibility.Collapsed : Visibility.Visible;
            }
        }

        [JsonIgnore]
        public string DisplayName
        {
            get
            {
                var baseDescr = !string.IsNullOrWhiteSpace(ExampleText) ? ExampleText : Language;
                return $"{baseDescr} ({Frequency})";
            }
            set
            {
               
            }
        }
    }
}
