namespace EmptyBins.View.UserPages;

using EmptyBins.Models;
using EmptyBins.Services;
using Microcharts;
using Microcharts.Maui;
using SkiaSharp;

public partial class StatScreen : ContentPage
{
    private UserDataService _userDataService;
    private AdviceModel AdviceModel;
    private UserData user;
    private PercentageModel p;


    public StatScreen()
	{
        _userDataService = new UserDataService();
        InitializeComponent();
   
        BindingContext = this;
      
	}

    protected override async void OnAppearing()
    {
        base.OnAppearing();
        await getUser();
        await FetchAIAdvice();
        InitializeChart();

    }

    private async Task FetchAIAdvice()
    {
        AdviceModel = await _userDataService.GetAIAdvice(user.id);
        p = await _userDataService.GetPercentage(user.id);
    }

    private async Task getUser()
    {
        user = await _userDataService.GetUserDataAsync();
    }

 
    private void InitializeChart()
    {
        // Példa adatok
        var entries = new List<ChartEntry>();
        var percentageEntries = new List<ChartEntry>();
        if (AdviceModel != null)
        {


            entries.Add(new ChartEntry(AdviceModel.expense) { Label = GetMonthName(AdviceModel.month), ValueLabel = AdviceModel.expense.ToString(), Color = SKColor.Parse("#266489") });

            
        }

        if (p != null)
        {


            percentageEntries.Add(new ChartEntry(p.comparison_for_user) { Label = "%", ValueLabel = p.comparison_for_user.ToString(), Color = SKColor.Parse("#266489") });

            
        }

      
        // Diagram létrehozása és beállítása
        var chart = new DonutChart{ Entries = entries };
        var chartPercentage = new PieChart { Entries = percentageEntries };
        this.chartView.Chart = chart;
        this.chartViewPercentage.Chart = chartPercentage;
    }


    public string GetMonthName(int monthNumber)
    {
        switch (monthNumber)
        {
            case 1:
                return "January";
            case 2:
                return "February";
            case 3:
                return "March";
            case 4:
                return "April";
            case 5:
                return "May";
            case 6:
                return "June";
            case 7:
                return "July";
            case 8:
                return "August";
            case 9:
                return "September";
            case 10:
                return "October";
            case 11:
                return "November";
            case 12:
                return "December";
            default:
                return "Invalid Month Number";
        }
    }



}