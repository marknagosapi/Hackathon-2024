using EmptyBins.Models;
using EmptyBins.Services;
using System.Collections.ObjectModel;

namespace EmptyBins.View.UserPages;

public partial class BillDetailScreen : ContentPage
{
    public ObservableCollection<ItemModel> Items { get; set; }
    private  BillDetailModel _billDetail;
    private UserDataService _userDataService;
    private int billID = 0;
  

    public BillDetailScreen(int bill_id)
    {

        InitializeComponent();
        _userDataService = new UserDataService();
        billID = bill_id;

        Items = new ObservableCollection<ItemModel>();

        // Set the BindingContext to this object
        this.BindingContext = this;
        ItemsCollectionView.ItemsSource = Items;
      

    }

    protected override async void OnAppearing()
    {
        base.OnAppearing();
        await FetchAndPopulateBills();

    }
    private async Task FetchAndPopulateBills()
    {
        // Call the GetUserBillsAsync method to fetch the bills
        _billDetail = await _userDataService.LoadBillDetails(billID);

        if (_billDetail != null)
        {
            totalItemsText.Text = _billDetail.item_number.ToString();
            totalPriceText.Text = _billDetail.total.ToString("C2");

            Items.Clear();

            foreach (var bill in _billDetail.items)
            {
                Items.Add(bill);
            }
        }
    }



}