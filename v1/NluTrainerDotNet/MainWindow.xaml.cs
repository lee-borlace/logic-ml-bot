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
        const string PythonExecutablePath = @"C:\Users\lborlace\AppData\Local\Continuum\anaconda3\envs\spacy\python.exe";
        const string TemplateFolder = @"C:\Users\lborlace\Documents\GitHub\Non-Forked\logic-ml-bot\v1\nlu_training_data_generator";

        //const string PythonExecutablePath = @"C:\Users\LeeBorlace\Anaconda3\envs\spacy\python.exe";
        //const string TemplateFolder = @"C:\Users\LeeBorlace\Documents\GitHub\logic-ml-bot\v1\nlu_training_data_generator";

        const string ScriptPath = @"sentence_analyzer_cmd_line.py";
        const string TemplateFile = @"training_templates.json";

        const bool StubJson = false;
        const string SampleJson = @"[{'t': 'the', 'l': 'the', 'p': 'DET', 'tg': 'DT'}, {'t': 'dog', 'l': 'dog', 'p': 'NOUN', 'tg': 'NN'}, {'t': 'ate', 'l': 'eat', 'p': 'VERB', 'tg': 'VBD'}, {'t': 'the', 'l': 'the', 'p': 'DET', 'tg': 'DT'}, {'t': 'cat', 'l': 'cat', 'p': 'NOUN', 'tg': 'NN'}]";

        private List<NlpToken> _tokensFromLastAnalysis;
        private List<TrainingExampleTemplate> _exampleTemplates;
        private LastFocusedControl _lastFocusedControl = LastFocusedControl.Language;

        private int _caretIndexLanguage = 0;
        private int _caretIndexLogic = 0;

        private bool _templatesDirty = false;

        private TrainingExampleTemplate _currentExample = null;

        const string PronHe = "He_DFJ8Y3T3";
        const string PronShe = "She_9DI3Y45D";
        const string PronIt = "It_2MB8D5E7";
        const string PronThey = "They_DJE9FIR2";
        const string PronListener = "Listener_HDI92HED";
        const string PronSpeaker = "Speaker_DH7WHD7D";

        public MainWindow()
        {
            InitializeComponent();
            cbSentenceType.Text = "Unknown";
        }

        private void BtnAnalyse_Click(object sender, RoutedEventArgs e)
        {
            var thread = new Thread(Analyse);
            thread.Start(txtInput.Text);
        }

        private void Analyse(object input)
        {
            var analysedJson = !StubJson ? RunPythonCommand(PythonExecutablePath, ScriptPath, $@"""{(string)input}""") : SampleJson;

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
            Log(analysedJson);
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
            try
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
            catch (Exception ex)
            {
                Log(ex);
                return string.Empty;
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
                if (_templatesDirty)
                {
                    var messageBoxResult = MessageBox.Show("There are unsaved template changes. Continue?", "Load Templates", System.Windows.MessageBoxButton.YesNo);
                    if (messageBoxResult == MessageBoxResult.No)
                    {
                        return;
                    }
                }

                using (StreamReader file = File.OpenText(System.IO.Path.Combine(TemplateFolder, TemplateFile)))
                {
                    JsonSerializer serializer = new JsonSerializer();
                    _exampleTemplates = (List<TrainingExampleTemplate>)serializer.Deserialize(file, typeof(List<TrainingExampleTemplate>));
                    Log($"Loaded {_exampleTemplates.Count} templates");

                    btnSaveTemplates.IsEnabled = true;
                    _templatesDirty = false;

                    dgTemplates.ItemsSource = _exampleTemplates;
                    _currentExample = null;
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
            try
            {
                string backedUpFileName = $"training_templates.{DateTime.Now.Ticks}.bak.json";
                File.Copy(System.IO.Path.Combine(TemplateFolder, TemplateFile), System.IO.Path.Combine(TemplateFolder, backedUpFileName), true);
                Log($"Backed up old templates to {backedUpFileName}.");

                var json = JsonConvert.SerializeObject(_exampleTemplates);
                System.IO.File.WriteAllText(System.IO.Path.Combine(TemplateFolder, TemplateFile), json);
                _templatesDirty = false;
                Log("Templates saved.");
            }
            catch (Exception ex)
            {
                Log(ex);
            }
        }

        #region Insert buttons

        private void BtnLeftBracket_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("(", false);
        }

        private void BtnRightBracket_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox(") ", false);
        }

        private void BtnImplies_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("=> ");
        }

        private void BtnComma_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox(", ", false);
        }

        private void BtnAnd_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("AND ");
        }

        private void BtnOr_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("OR ");
        }

        private void BtnNot_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("NOT ");
        }

        private void BtnConst1_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("Const1, ");
        }

        private void BtnConst2_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("Const2, ");
        }

        private void BtnConst3_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("Const3, ");
        }

        private void BtnConst4_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("Const4, ");
        }

        private void BtnConst5_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("Const5, ");
        }

        private void BtnConst6_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("Const6, ");
        }

        private void BtnX_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("x, ", capitaliseForLogicBox: false);
        }

        private void BtnY_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("y, ", capitaliseForLogicBox: false);
        }

        private void BtnZ_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("z, ", capitaliseForLogicBox: false);
        }

        private void BtnA_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("a, ", capitaliseForLogicBox: false);
        }

        private void BtnB_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("b, ", capitaliseForLogicBox: false);
        }

        private void BtnC_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("c, ", capitaliseForLogicBox: false);
        }

        private void BtnInstance_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("Instance(");
        }

        private void BtnVerb_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("Verb(");
        }

        private void BtnAdverb_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("Adverb(");
        }

        private void BtnVerbTense_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("VerbTense(");
        }

        private void BtnAdjective_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox("Adjective(");
        }

        private void BtnSpeaker_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox($"{PronSpeaker}, ");
        }

        private void BtnListener_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox($"{PronListener}, ");
        }

        private void BtnHe_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox($"{PronHe}, ");
        }

        private void BtnShe_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox($"{PronShe}, ");
        }

        private void BtnIt_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox($"{PronIt}, ");
        }

        private void BtnThey_Click(object sender, RoutedEventArgs e)
        {
            _lastFocusedControl = LastFocusedControl.Logic;
            InsertToSelectedTextBox($"{PronThey}, ");
        }

        void InsertToSelectedTextBox(string textToInsert, bool mayHaveSpaceBefore = true, bool capitaliseForLogicBox = true)
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

                    if (capitaliseForLogicBox)
                    {
                        if (textToInsert.Length == 1)
                        {
                            textToInsert = textToInsert.First().ToString().ToUpper();
                        }
                        else
                        {
                            textToInsert = textToInsert.First().ToString().ToUpper() + textToInsert.Substring(1);
                        }
                    }
                }

                if (textToInsert == ") ")
                {
                    if (textBox.Text.Length >= 2 && textBox.Text.EndsWith(", "))
                    {
                        textBox.Text = textBox.Text.Substring(0, textBox.Text.Length - 2);
                    }

                    if (textBox.Text.Length >= 2 && textBox.Text.EndsWith(", "))
                    {
                        textBox.Text = textBox.Text.Substring(0, textBox.Text.Length - 1);
                    }

                    if (textBox.Text.Length >= 1 && textBox.Text.EndsWith(","))
                    {
                        textBox.Text = textBox.Text.Substring(0, textBox.Text.Length);
                    }
                }

                var origCaratIndex = indexToInsertInto;

                if (!mayHaveSpaceBefore)
                {
                    textBox.Text.TrimEnd();
                }

                indexToInsertInto = Math.Min(indexToInsertInto, textBox.Text.Length);

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

        #region  Analysis data grid

        private void DgAddTextLemma(object sender, RoutedEventArgs e)
        {
            try
            {
                for (var vis = sender as Visual; vis != null; vis = VisualTreeHelper.GetParent(vis) as Visual)
                {
                    if (vis is DataGridRow)
                    {
                        var row = (DataGridRow)vis;
                        var token = row.DataContext as NlpToken;

                        switch (_lastFocusedControl)
                        {
                            case LastFocusedControl.Language:
                                InsertToSelectedTextBox(token.TextContent + " ");
                                break;
                            case LastFocusedControl.Logic:
                                InsertToSelectedTextBox(token.Lemma + " ");
                                break;
                        }

                        break;
                    }
                }
            }
            catch (Exception ex)
            {
                Log(ex);
            }
        }

        private void DgAddPos(object sender, RoutedEventArgs e)
        {
            try
            {
                for (var vis = sender as Visual; vis != null; vis = VisualTreeHelper.GetParent(vis) as Visual)
                {
                    if (vis is DataGridRow)
                    {
                        var row = (DataGridRow)vis;
                        var token = row.DataContext as NlpToken;

                        switch(_lastFocusedControl)
                        {
                            case LastFocusedControl.Language:
                                InsertToSelectedTextBox(token.TokenForLanguage + " ");
                                break;
                            case LastFocusedControl.Logic:
                                InsertToSelectedTextBox(token.TokenForLogic + " ");
                                break;
                        }

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

        #region  Template data grid

        private void DgTemplateSelect(object sender, RoutedEventArgs e)
        {
            try
            {
                for (var vis = sender as Visual; vis != null; vis = VisualTreeHelper.GetParent(vis) as Visual)
                {
                    if (vis is DataGridRow)
                    {
                        var row = (DataGridRow)vis;
                        var template = row.DataContext as TrainingExampleTemplate;

                        _currentExample = template;

                        txtInput.Text = _currentExample.ExampleText;
                        txtExampleLanguage.Text = _currentExample.Language;
                        txtExampleLogic.Text = _currentExample.Logic;
                        cbSentenceType.Text = !string.IsNullOrWhiteSpace(_currentExample.SentenceType) ? _currentExample.SentenceType : "Unknown";
                        dgTokens.ItemsSource = new List<NlpToken>();
                        cbFrequency.Text = _currentExample.Frequency.ToString();

                        SetUpSaveInsertButton();

                        break;
                    }
                }
            }
            catch (Exception ex)
            {
                Log(ex);
            }
        }

        private void DgTemplateDelete(object sender, RoutedEventArgs e)
        {
            try
            {
                for (var vis = sender as Visual; vis != null; vis = VisualTreeHelper.GetParent(vis) as Visual)
                {
                    if (vis is DataGridRow)
                    {
                        var row = (DataGridRow)vis;
                        var template = row.DataContext as TrainingExampleTemplate;

                        var messageBoxResult = System.Windows.MessageBox.Show("Delete template?", "Delete Template", System.Windows.MessageBoxButton.YesNo);

                        if (messageBoxResult == MessageBoxResult.Yes)
                        {
                            _currentExample = null;
                            txtInput.Text = string.Empty;
                            txtExampleLanguage.Text = string.Empty;
                            txtExampleLogic.Text = string.Empty;
                            dgTokens.ItemsSource = new List<NlpToken>();

                            _exampleTemplates = _exampleTemplates.Where(t => t.Id != template.Id).ToList();
                            dgTemplates.ItemsSource = null;
                            dgTemplates.ItemsSource = _exampleTemplates;
                            _templatesDirty = true;

                            _currentExample = null;

                            SetUpSaveInsertButton();
                        }

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

        #region Example CRUD

        private void SetUpSaveInsertButton()
        {
            if (_currentExample == null)
            {
                btnSaveInsert.Content = "Insert Example";
            }
            else
            {
                btnSaveInsert.Content = "Save Example";
            }
        }

        private void BtnNewExample_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                _currentExample = null;
                txtInput.Text = string.Empty;
                txtExampleLanguage.Text = string.Empty;
                txtExampleLogic.Text = string.Empty;
                cbSentenceType.Text = "Unknown";
                dgTokens.ItemsSource = null;
                dgTokens.ItemsSource = new List<NlpToken>();
                cbFrequency.Text = "5";
                SetUpSaveInsertButton();
            }
            catch (Exception ex)
            {
                Log(ex);
            }
        }


        private void BtnSaveInsert_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                // Do some cleanup
                txtExampleLogic.Text = txtExampleLogic.Text.Replace(",)", ")");
                txtExampleLogic.Text = txtExampleLogic.Text.Replace(", )", ")");
                txtExampleLogic.Text = txtExampleLogic.Text.Replace(",  )", ")");

                // Do some validation.
                if (txtExampleLogic.Text.Count(f => f == '(') != txtExampleLogic.Text.Count(f => f == ')'))
                {
                    MessageBox.Show("Bracket mismatch in logic example!");
                    return;
                }

                if ((string.IsNullOrWhiteSpace(txtExampleLanguage.Text) || string.IsNullOrWhiteSpace(txtExampleLogic.Text)) && string.IsNullOrWhiteSpace(txtInput.Text))
                {
                    MessageBox.Show("If you don't specify language or logic, then you must specify example!");
                    return;
                }

                if (_exampleTemplates == null)
                {
                    LoadTemplates();
                }

                if (_currentExample != null)
                {
                    _templatesDirty = true;

                    var existingTemplate = _exampleTemplates.First(t => t.Id == _currentExample.Id);

                    _currentExample.ExampleText = txtInput.Text;
                    _currentExample.Language = existingTemplate.Language = txtExampleLanguage.Text.Trim();
                    _currentExample.Logic = existingTemplate.Logic = txtExampleLogic.Text.Trim();
                    _currentExample.SentenceType = cbSentenceType.Text;

                    int.TryParse(cbFrequency.Text, out int frequency);
                    _currentExample.Frequency = frequency;

                    dgTemplates.ItemsSource = null;
                    dgTemplates.ItemsSource = _exampleTemplates;

                    SetUpSaveInsertButton();
                }
                else
                {
                    _templatesDirty = true;

                    int.TryParse(cbFrequency.Text, out int frequency);

                    _currentExample = new TrainingExampleTemplate()
                    {
                        Id = Guid.NewGuid().ToString(),
                        Language = txtExampleLanguage.Text.Trim(),
                        Logic = txtExampleLogic.Text.Trim(),
                        SentenceType = cbSentenceType.Text,
                        ExampleText = txtInput.Text,
                        Frequency = frequency
                    };

                    _exampleTemplates.Add(_currentExample);

                    dgTemplates.ItemsSource = null;
                    dgTemplates.ItemsSource = _exampleTemplates;


                    SetUpSaveInsertButton();
                }
            }
            catch (Exception ex)
            {
                Log(ex);
            }
        }

        #endregion


        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            if (_templatesDirty)
            {
                var messageBoxResult = System.Windows.MessageBox.Show("Are you sure? Templates are not saved.", "Close Window", System.Windows.MessageBoxButton.YesNo);

                if (messageBoxResult == MessageBoxResult.No)
                {
                    e.Cancel = true;
                }
            }
        }


    }
}
