using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EmptyBins.Models
{
    public class UserData
    {
        public string first_name { get; set; }
        public string last_name { get; set; }
        public string email { get; set; }
        public int points { get; set; }
        public int? level_id { get; set; }
    }

}