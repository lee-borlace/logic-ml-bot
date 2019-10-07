using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NluTrainerDotNet.Model
{
    public class NlpToken
    {
        [JsonProperty("t")]
        public string TextContent { get; set; }

        [JsonProperty("l")]
        public string Lemma { get; set; }

        [JsonProperty("p")]
        public string Pos { get; set; }

        [JsonProperty("tg")]
        public string Tag { get; set; }

        /// <summary>
        /// Token to be used for language example, containing POS, index and tag, separated by underscore, e.g. NOUN_3_NN
        /// </summary>
        public string TokenForLanguage { get; set; }

        public string TokenForLanguageForButton
        {
            get
            {
                return TokenForLanguage.Replace("_", "__");
            }
        }

        /// <summary>
        /// Token to be used for logic example, containing POS and index, but no tag. E.g. NOUN_3
        /// </summary>
        public string TokenForLogic { get; set; }

        public string TokenForLogicForButton
        {
            get
            {
                return TokenForLogic.Replace("_", "__");
            }
        }


    }
}
