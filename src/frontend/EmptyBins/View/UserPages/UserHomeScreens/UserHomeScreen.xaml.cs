
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Windows.Input;
using EmptyBins.Models;
using EmptyBins.Services;
using EmptyBins.View.AuthPages;
using EmptyBins.View.UserPages;
namespace EmptyBins.View.UserPages;

[XamlCompilation(XamlCompilationOptions.Compile)]
public partial class UserHomeScreen : ContentPage, INotifyPropertyChanged

{
    private UserDataService _userDataService;
    private string _username = "";
    private int _score = 15125;

    public ObservableCollection<BillModel> Bills { get; set; }
    public ICommand OnBillTappedCommand { get; private set; }

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
        // Initialize the command


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

    private async void OnItemTapped(object sender, EventArgs e)
    {
        var tappedFrame = sender as Frame;
        if (tappedFrame != null)
        {
            var tappedBill = tappedFrame.BindingContext as BillModel;
            if (tappedBill != null)
            {
                // Access the id of the tapped bill and do something with it
                var billId = tappedBill.id;
              
                await Navigation.PushAsync(new BillDetailScreen(billId));
            }
        }
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

    private async void OnStatisticsClicked(object sender, EventArgs e)
    {
        // Navigálás a ScanQRCodeScreen-re
        await Navigation.PushAsync(new StatScreen());
    }

}
