using Newtonsoft.Json;
using NluTrainerDotNet.Model;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace NluTrainerDotNet
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        const string PythonPath = @"C:\Users\LeeBorlace\Anaconda3\envs\spacy\python.exe";
        const string ScriptPath = @"C:\Users\LeeBorlace\Documents\GitHub\logic-ml-bot\v1\NluTrainerDotNet\sentence_analyzer_cmd_line.py";
        const string TemplatePath = @"C:\Users\LeeBorlace\Documents\GitHub\logic-ml-bot\v1\nlu_training_data_generator\training_templates.json";

        const bool StubJson = true;
        const string SampleJson = @"[{'t': 'the', 'l': 'the', 'p': 'DET', 'tg': 'DT'}, {'t': 'dog', 'l': 'dog', 'p': 'NOUN', 'tg': 'NN'}, {'t': 'ate', 'l': 'eat', 'p': 'VERB', 'tg': 'VBD'}, {'t': 'the', 'l': 'the', 'p': 'DET', 'tg': 'DT'}, {'t': 'cat', 'l': 'cat', 'p': 'NOUN', 'tg': 'NN'}]";

        private List<NlpToken> _tokensFromLastAnalysis;
        private List<TrainingExampleTemplate> _exampleTemplates;
        private LastFocusedControl _lastFocusedControl = LastFocusedControl.Language;

        public MainWindow()
        {
            InitializeComponent();
        }

        private void BtnAnalyse_Click(object sender, RoutedEventArgs e)
        {
            var thread = new Thread(Analyse);
            thread.Start(txtInput.Text);
        }

        private void Analyse(object input)
        {
            Dispatcher.BeginInvoke(new Action(() =>
            {
                txtOutput.Text = "Analysing...";
            }));

            var analysedJson = !StubJson ? RunPythonCommand(PythonPath, ScriptPath, $@"""{(string)input}""") : SampleJson;

            if (string.IsNullOrEmpty(analysedJson))
            {
                analysedJson = "(No result)";
            }

            Dispatcher.BeginInvoke(new Action(() =>
            {
                HandleAnalysisResponse(analysedJson);
            }));

        }

        private void HandleAnalysisResponse(string analysedJson)
        {
            analysedJson = analysedJson.Trim();
            txtOutput.Text = analysedJson;

            try
            {
                _tokensFromLastAnalysis = JsonConvert.DeserializeObject<List<NlpToken>>(analysedJson);
            }
            catch(Exception ex)
            {
                MessageBox.Show($"Error processing analysis result - {ex.Message}");
                return;
            }
        }

        private string RunPythonCommand(string pythonPath, string commandPath, string args)
        {
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = pythonPath;
            start.Arguments = $"{commandPath} {args}";
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;

            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    return reader.ReadToEnd();
                }
            }
        }

        private void BtnLoadTemplates_Click(object sender, RoutedEventArgs e)
        {
            var thread = new Thread(LoadTemplates);
            thread.Start();
        }

        private void LoadTemplates()
        {
            try
            {
                using (StreamReader file = File.OpenText(TemplatePath))
                {
                    JsonSerializer serializer = new JsonSerializer();
                    _exampleTemplates = (List<TrainingExampleTemplate>)serializer.Deserialize(file, typeof(List<TrainingExampleTemplate>));
                }
            }
            catch(Exception ex)
            {
                MessageBox.Show($"Error loading templates - {ex.Message}");
            }
        }

        private void TxtExampleLanguage_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Language;
        }

        private void TxtExampleLogic_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
        }
    }
}
