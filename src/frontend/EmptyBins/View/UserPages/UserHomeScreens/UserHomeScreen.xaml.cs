using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using EmptyBins.Models;
using EmptyBins.Services;
using EmptyBins.View.AuthPages;
namespace EmptyBins.View.UserPages;


public partial class UserHomeScreen : ContentPage, INotifyPropertyChanged

{
    private UserDataService _userDataService;
    private string _username = "";
    private int _score = 15125;

    public ObservableCollection<BillModel> Bills { get; set; }

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
        _userDataService = new UserDataService();
        InitializeComponent();

        Bills = new ObservableCollection<BillModel>();

        // Set the BindingContext to this object
        this.BindingContext = this;

    }

    protected override async void OnAppearing()
    {
        base.OnAppearing();

        await FetchUserDataAsync();
        await FetchAndPopulateBills();
    }


    public event PropertyChangedEventHandler PropertyChanged;

    private async void OnIconTapped(object sender, EventArgs e)
    {
        // Navigate to your desired page when the icon is tapped
         await Navigation.PushAsync(new BillDetailScreen(sender.));
    }

    private async void OnStackLayoutTapped(object sender, EventArgs e)
    {
        // Navigate to your desired page when the stack layout is tapped
        await Navigation.PushAsync(new BillDetailScreen(1));

    }

    private async void OnTotalLabelTapped(object sender, EventArgs e)
    {
        // Navigate to your desired page when the total label is tapped
        await Navigation.PushAsync(new BillDetailScreen(1));

    }

    private async Task FetchAndPopulateBills()
    {
        // Call the GetUserBillsAsync method to fetch the bills
        var userBills = await _userDataService.GetUserBillsAsync();

        if (userBills != null)
        {
      
            Bills.Clear();

            foreach (var bill in userBills)
            {
                Bills.Add(bill);
            }
        }
    }

    public async Task FetchUserDataAsync()
    {
        try
        {
            var userData = await _userDataService.GetUserDataAsync();

            if (userData != null)
            {
          
                Username = userData.last_name + " " + userData.first_name;
                Score = userData.points;

            }
            else
            {
                Username = "b";
     
            }
        }
        catch (Exception ex)
        {
        }
    }

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

    private async void OnLogOutClicked(object sender, EventArgs e)
    {
        // Navigálás a ScanQRCodeScreen-re
        await Navigation.PushAsync(new LoginScreen());
    }

}

