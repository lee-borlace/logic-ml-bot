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
        public string Text { get; set; }

        [JsonProperty("l")]
        public string Lemma { get; set; }

        [JsonProperty("p")]
        public string Pos { get; set; }

        [JsonProperty("tg")]
        public string Tag { get; set; }
    }
}
