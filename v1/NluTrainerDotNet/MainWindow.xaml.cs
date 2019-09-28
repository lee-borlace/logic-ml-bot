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
        // Make sure the environment that this python.exe is in contains required libs
        const string PythonPath = @"C:\Users\LeeBorlace\Anaconda3\envs\spacy\python.exe";
        const string ScriptPath = @"C:\Users\LeeBorlace\Documents\GitHub\logic-ml-bot\v1\NluTrainerDotNet\sentence_analyzer_cmd_line.py";

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

            var result = RunPythonCommand(PythonPath, ScriptPath, $@"""{(string)input}""");

            if (string.IsNullOrEmpty(result))
            {
                result = "(No result)";
            }

            Dispatcher.BeginInvoke(new Action(() =>
            {
                txtOutput.Text = result;
            }));

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


    }
}
