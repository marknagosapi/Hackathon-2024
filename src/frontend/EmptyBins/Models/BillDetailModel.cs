using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EmptyBins.Models
{
    public class BillDetailModel
    {

        public int user_id { get; set; }
        public int admin_id { get; set; }
        public string date { get; set; }
        public int item_number { get; set; }
        public string market_name {  get; set; }
        public float total { get; set; }
        public ItemModel[] items { get; set; }

    }
}