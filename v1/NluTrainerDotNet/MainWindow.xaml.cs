using Newtonsoft.Json;
using NluTrainerDotNet.Model;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Data;
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

        private int _caretIndexLanguage = 0;
        private int _caretIndexLogic = 0;

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
                SetUpShortcutButtons();
            }));

        }

        private void SetUpShortcutButtons()
        {

        }

        private void HandleAnalysisResponse(string analysedJson)
        {
            analysedJson = analysedJson.Trim();
            txtOutput.Text = analysedJson;
            Log("Analysis complete.");

            try
            {
                _tokensFromLastAnalysis = JsonConvert.DeserializeObject<List<NlpToken>>(analysedJson);

                // Keep track of index of each POS encountered.
                var posCountDict = new Dictionary<string, int>();

                // Set up tokens so they can be used by language and logic examples.
                foreach (var token in _tokensFromLastAnalysis)
                {
                    var pos = token.Pos;
                    var tag = token.Tag;

                    if (!posCountDict.ContainsKey(pos))
                    {
                        posCountDict[pos] = 1;
                    }
                    else
                    {
                        posCountDict[pos]++;
                    }

                    // Remember, 1-based index!
                    token.TokenForLanguage = $"{pos}_{posCountDict[pos]}_{tag}";
                    token.TokenForLogic = $"{pos}_{posCountDict[pos]}";
                }

                dgTokens.ItemsSource = _tokensFromLastAnalysis;
            }
            catch (Exception ex)
            {
                Log(ex);
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
            LoadTemplates();
        }

        private void LoadTemplates()
        {
            try
            {
                string backedUpFileName = $"training_templates.{DateTime.Now.Ticks}.bak.json";
                File.Copy(TemplatePath, backedUpFileName, true);

                using (StreamReader file = File.OpenText(TemplatePath))
                {
                    JsonSerializer serializer = new JsonSerializer();
                    _exampleTemplates = (List<TrainingExampleTemplate>)serializer.Deserialize(file, typeof(List<TrainingExampleTemplate>));
                    Log($"Loaded {_exampleTemplates.Count} templates");
                    Log($"Backed up old templates to {backedUpFileName}.");

                    btnSaveTemplates.IsEnabled = true;
                }
            }
            catch (Exception ex)
            {
                Log(ex);
            }
        }

        private void TxtExampleLanguage_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            UpdateCaretIndexes();
            _lastFocusedControl = LastFocusedControl.Language;
        }

        private void TxtExampleLogic_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            UpdateCaretIndexes();
            _lastFocusedControl = LastFocusedControl.Logic;
        }

        private void UpdateCaretIndexes()
        {
            _caretIndexLanguage = txtExampleLanguage.CaretIndex;
            _caretIndexLogic = txtExampleLogic.CaretIndex;
        }

        private void Log(string msg)
        {
            Dispatcher.BeginInvoke(new Action(() =>
            {
                txtLog.Text += System.Environment.NewLine + msg;
            }));
        }

        private void Log(Exception ex)
        {
            Dispatcher.BeginInvoke(new Action(() =>
            {
                txtLog.Text += System.Environment.NewLine + ex.GetType();
                txtLog.Text += System.Environment.NewLine + ex.Message;
                txtLog.Text += System.Environment.NewLine + ex.StackTrace;
                txtLog.ScrollToEnd();
            }));
        }

        private void ButtonSaveTemplates_Click(object sender, RoutedEventArgs e)
        {
            var messageBoxResult = System.Windows.MessageBox.Show("Overwrite templates?", "Save Templates", System.Windows.MessageBoxButton.YesNo);

            if (messageBoxResult == MessageBoxResult.Yes)
            {
                var json = JsonConvert.SerializeObject(_exampleTemplates);
                System.IO.File.WriteAllText(TemplatePath, json);
                Log("Templates saved.");
            }
        }

        #region Insert buttons

        private void BtnLeftBracket_Click(object sender, RoutedEventArgs e)
        {
            InsertToSelectedTextBox("(", false);
        }

        private void BtnRightBracket_Click(object sender, RoutedEventArgs e)
        {
            InsertToSelectedTextBox(") ", false);
        }

        private void BtnImplies_Click(object sender, RoutedEventArgs e)
        {
            InsertToSelectedTextBox("=> ");
        }

        private void BtnComma_Click(object sender, RoutedEventArgs e)
        {
            InsertToSelectedTextBox(", ", false);
        }

        private void BtnAnd_Click(object sender, RoutedEventArgs e)
        {
            InsertToSelectedTextBox("AND ");
        }

        private void BtnOr_Click(object sender, RoutedEventArgs e)
        {
            InsertToSelectedTextBox("OR ");
        }

        private void BtnNot_Click(object sender, RoutedEventArgs e)
        {
            InsertToSelectedTextBox("NOT ");
        }

        private void BtnConst1_Click(object sender, RoutedEventArgs e)
        {
            InsertToSelectedTextBox("Const1");
        }

        private void BtnConst2_Click(object sender, RoutedEventArgs e)
        {
            InsertToSelectedTextBox("Const2");
        }

        private void BtnConst3_Click(object sender, RoutedEventArgs e)
        {
            InsertToSelectedTextBox("Const3");
        }

        private void BtnConst4_Click(object sender, RoutedEventArgs e)
        {
            InsertToSelectedTextBox("Const4");
        }

        private void BtnConst5_Click(object sender, RoutedEventArgs e)
        {
            InsertToSelectedTextBox("Const5");
        }

        private void BtnConst6_Click(object sender, RoutedEventArgs e)
        {
            InsertToSelectedTextBox("Const6");
        }

        private void BtnX_Click(object sender, RoutedEventArgs e)
        {
            InsertToSelectedTextBox("x");
        }

        private void BtnY_Click(object sender, RoutedEventArgs e)
        {
            InsertToSelectedTextBox("y");
        }

        private void BtnZ_Click(object sender, RoutedEventArgs e)
        {
            InsertToSelectedTextBox("z");
        }

        private void BtnA_Click(object sender, RoutedEventArgs e)
        {
            InsertToSelectedTextBox("a");
        }

        private void BtnB_Click(object sender, RoutedEventArgs e)
        {
            InsertToSelectedTextBox("b");
        }

        private void BtnC_Click(object sender, RoutedEventArgs e)
        {
            InsertToSelectedTextBox("c");
        }

        void InsertToSelectedTextBox(string textToInsert, bool mayHaveSpaceBefore = true)
        {
            try
            {
                UpdateCaretIndexes();

                TextBox textBox;

                var indexToInsertInto = 0;

                if (_lastFocusedControl == LastFocusedControl.Language)
                {
                    textBox = txtExampleLanguage;
                    indexToInsertInto = _caretIndexLanguage;
                }
                else
                {
                    textBox = txtExampleLogic;
                    indexToInsertInto = _caretIndexLogic;
                }

                var origCaratIndex = indexToInsertInto;

                if (!mayHaveSpaceBefore)
                {
                    textBox.Text.TrimEnd();
                }

                if (textBox.Text.Length > 0)
                {
                    var textBeforeInsert = textBox.Text.Substring(0, indexToInsertInto);
                    var textAfterInsert = textBox.Text.Substring(indexToInsertInto);
                    textBox.Text = textBeforeInsert + textToInsert + textAfterInsert;
                }
                else
                {
                    textBox.Text = textToInsert;
                }

                textBox.CaretIndex = origCaratIndex + textToInsert.Length;
            }
            catch (Exception ex)
            {
                Log(ex);
            }
        }

        #endregion

        #region  Data grid

        private void DgAddText(object sender, RoutedEventArgs e)
        {
            try
            {
                for (var vis = sender as Visual; vis != null; vis = VisualTreeHelper.GetParent(vis) as Visual)
                {
                    if (vis is DataGridRow)
                    {
                        var row = (DataGridRow)vis;
                        var token = row.DataContext as NlpToken;

                        InsertToSelectedTextBox(token.Text + " ");

                        break;
                    }
                }
            }
            catch (Exception ex)
            {
                Log(ex);
            }
        }

        private void DgAddLemma(object sender, RoutedEventArgs e)
        {
            try
            {
                for (var vis = sender as Visual; vis != null; vis = VisualTreeHelper.GetParent(vis) as Visual)
                {
                    if (vis is DataGridRow)
                    {
                        var row = (DataGridRow)vis;
                        var token = row.DataContext as NlpToken;

                        InsertToSelectedTextBox(token.Lemma + " ");

                        break;
                    }
                }
            }
            catch (Exception ex)
            {
                Log(ex);
            }
        }

        private void DgAddLanguageToken(object sender, RoutedEventArgs e)
        {
            try
            {
                for (var vis = sender as Visual; vis != null; vis = VisualTreeHelper.GetParent(vis) as Visual)
                {
                    if (vis is DataGridRow)
                    {
                        var row = (DataGridRow)vis;
                        var token = row.DataContext as NlpToken;

                        InsertToSelectedTextBox(token.TokenForLanguage + " ");

                        break;
                    }
                }
            }
            catch (Exception ex)
            {
                Log(ex);
            }
        }

        private void DgAddLogicToken(object sender, RoutedEventArgs e)
        {
            try
            {
                for (var vis = sender as Visual; vis != null; vis = VisualTreeHelper.GetParent(vis) as Visual)
                {
                    if (vis is DataGridRow)
                    {
                        var row = (DataGridRow)vis;
                        var token = row.DataContext as NlpToken;

                        InsertToSelectedTextBox(token.TokenForLogic + " ");

                        break;
                    }
                }
            }
            catch (Exception ex)
            {
                Log(ex);
            }
        }

        #endregion
    }
}
