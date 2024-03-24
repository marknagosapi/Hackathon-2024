using Microcharts;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EmptyBins.Converter
{
    public class ImageConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            if (value is int)
            {

                if (value is int score && score < 500)
                {
                    // Return the image path for scores greater than 500
                    return ImageSource.FromFile("tree1.png");
                }
                else if (value is int scor2 && scor2 >= 500)
                {
                    return ImageSource.FromFile("tree2.png");


                }
                else
                {
                    return ImageSource.FromFile("tree3.png");

                }
               
            }
            return null;
        }

        public object ConvertBack(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
}