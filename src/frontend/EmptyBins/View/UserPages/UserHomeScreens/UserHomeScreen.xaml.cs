using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace EmptyBins.View.UserPages;

public partial class UserHomeScreen : ContentPage, INotifyPropertyChanged
{

    private string _username = "DummyUser";
    private int _score = 15125;

    public ObservableCollection<Bill> Bills { get; set; }

    public string Username
    {
        get => _username;
        set => SetProperty(ref _username, value);
    }

    public int Score
    {
        get => _score;
        set => SetProperty(ref _score, value);
    }

    public UserHomeScreen()
    {
        InitializeComponent();
        Bills = new ObservableCollection<Bill>()
            {
                new Bill { MarketName = "Market A", TotalSum = "100.00", DateTime = "2023-03-22" },
                new Bill { MarketName = "Market B", TotalSum = "1244.00", DateTime = "2023-03-2" },
                new Bill { MarketName = "Market C", TotalSum = "1230.00", DateTime = "2023-02-12" },
                new Bill { MarketName = "Market D", TotalSum = "10.00", DateTime = "2023-01-11" },
                new Bill { MarketName = "Market E", TotalSum = "130.00", DateTime = "2023-01-4" },
                // Add more dummy data here

            };
        this.BindingContext = this;
    }

    public event PropertyChangedEventHandler PropertyChanged;

    protected virtual void OnPropertyChanged([CallerMemberName] string propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    protected bool SetProperty<T>(ref T storage, T value, [CallerMemberName] string propertyName = null)
    {
        if (Equals(storage, value))
        {
            return false;
        }

        storage = value;
        OnPropertyChanged(propertyName);
        return true;
    }

    private async void OnScanQRCodeClicked(object sender, EventArgs e)
    {
        // Navigálás a ScanQRCodeScreen-re
        await Navigation.PushAsync(new ScanQRCodeScreen());
    }

    public class Bill
    {
        public string MarketName { get; set; }
        public string TotalSum { get; set; }
        public string DateTime { get; set; }
    }
}

