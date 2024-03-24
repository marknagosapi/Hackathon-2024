using EmptyBins.Models;
using Newtonsoft.Json;
using System;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace EmptyBins.Services
{
    public class UserDataService
    {
        private const string ApiBaseUrl = "http://localhost:8000";
        private readonly HttpClient _httpClient;
        private BillDetailModel _billDetail;

        public UserDataService()
        {
            _httpClient = new HttpClient();
            _httpClient.BaseAddress = new Uri(ApiBaseUrl); // Set the base address
        }

        public async Task<UserData> GetUserDataAsync()
        {
            try
            {
                // Retrieve the token from SecretsStorage
                var tokenResponseJson = await SecureStorage.GetAsync("AccessToken");


                // Ensure token exists
                if (string.IsNullOrWhiteSpace(tokenResponseJson))
                {
                    throw new InvalidOperationException("Token response not found in SecretsStorage.");
                }


                // Add token to request headers
                _httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", tokenResponseJson);

                var response = await _httpClient.GetAsync("/users/me/");

                // Check status code
                if (response.IsSuccessStatusCode)
                {
                    using (var responseStream = await response.Content.ReadAsStreamAsync())
                    {
                        using (var streamReader = new StreamReader(responseStream))
                        using (var jsonReader = new JsonTextReader(streamReader))
                        {
                            var serializer = new JsonSerializer();
                            var userData = serializer.Deserialize<UserData>(jsonReader);
                            return userData;
                        }
                    }
                }
                else
                {
                    // Handle unsuccessful response
                    Console.WriteLine($"Failed to fetch user data. Status code: {response.StatusCode}");
                }
            }
            catch (Exception ex)
            {
                // Handle exceptions
                Console.WriteLine($"An error occurred: {ex.Message}");
            }

            return null;
        }


        public async Task<List<BillModel>> GetUserBillsAsync()
        {
            try
            {

                var token = await SecureStorage.GetAsync("AccessToken");

                // Ensure token exists
                if (string.IsNullOrWhiteSpace(token))
                {
                    throw new InvalidOperationException("Access token not found in SecretsStorage.");
                }


                _httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

                var response = await _httpClient.GetAsync("/users/me/bills/");

                // Check status code
                if (response.IsSuccessStatusCode)
                {
                    var json = await response.Content.ReadAsStringAsync();
                    var bills = JsonConvert.DeserializeObject<List<BillModel>>(json);
                    return bills;
                }
                else
                {

                    Console.WriteLine($"Failed to fetch user bills. Status code: {response.StatusCode}");
                }
            }
            catch (Exception ex)
            {
                // Handle exceptions
                Console.WriteLine($"An error occurred: {ex.Message}");
            }

            return null;
        }

        public async Task<BillDetailModel> LoadBillDetails(int billId)
        {
            try
            {
                // Retrieve the token from SecretsStorage
                var token = await SecureStorage.GetAsync("AccessToken");

                // Ensure token exists
                if (string.IsNullOrWhiteSpace(token))
                {
                    throw new InvalidOperationException("Access token not found in SecretsStorage.");
                }

                // Add token to request headers
                _httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

                var response = await _httpClient.GetAsync($"/users/me/bill_by_id/?bill_id={billId}");

                // Check status code
                if (response.IsSuccessStatusCode)
                {
                    var json = await response.Content.ReadAsStringAsync();
                    var billDetail = Newtonsoft.Json.JsonConvert.DeserializeObject<BillDetailModel>(json);

                    return billDetail;
                }
                else
                {
                    // Handle unsuccessful response
                    Console.WriteLine($"Failed to fetch bill details. Status code: {response.StatusCode}");
                    // Optionally throw an exception or return a specific response object to indicate failure
                    return null;
                }
            }
            catch (Exception ex)
            {
                // Handle exceptions
                Console.WriteLine($"An error occurred: {ex.Message}");
                // Optionally throw an exception or return a specific response object to indicate failure
                return null;
            }
        }

        public async Task<AdviceModel> GetAIAdvice(int userID)
        {
            try
            {
                // Retrieve the token from SecretsStorage
                var tokenResponseJson = await SecureStorage.GetAsync("AccessToken");

           


                // Ensure token exists
                if (string.IsNullOrWhiteSpace(tokenResponseJson))
                {
                    throw new InvalidOperationException("Token response not found in SecretsStorage.");
                }


                // Add token to request headers
                _httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", tokenResponseJson);

                var response = await _httpClient.GetAsync($"/next_month_expenses/{userID}");

                // Check status code
                if (response.IsSuccessStatusCode)
                {
                    using (var responseStream = await response.Content.ReadAsStreamAsync())
                    {
                        using (var streamReader = new StreamReader(responseStream))
                        using (var jsonReader = new JsonTextReader(streamReader))
                        {
                            var serializer = new JsonSerializer();
                            var userData = serializer.Deserialize<AdviceModel>(jsonReader);
                            return userData;
                        }
                    }
                }
                else
                {
                    // Handle unsuccessful response
                    Console.WriteLine($"Failed to fetch user data. Status code: {response.StatusCode}");
                }
            }
            catch (Exception ex)
            {
                // Handle exceptions
                Console.WriteLine($"An error occurred: {ex.Message}");
            }

            return null;
        }

        public async Task<PercentageModel> GetPercentage(int userID)
        {
            try
            {
                // Retrieve the token from SecretsStorage
                var tokenResponseJson = await SecureStorage.GetAsync("AccessToken");



                // Ensure token exists
                if (string.IsNullOrWhiteSpace(tokenResponseJson))
                {
                    throw new InvalidOperationException("Token response not found in SecretsStorage.");
                }


                // Add token to request headers
                _httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", tokenResponseJson);

                var response = await _httpClient.GetAsync($"/comparison_for_user/{userID}");

                // Check status code
                if (response.IsSuccessStatusCode)
                {
                    using (var responseStream = await response.Content.ReadAsStreamAsync())
                    {
                        using (var streamReader = new StreamReader(responseStream))
                        using (var jsonReader = new JsonTextReader(streamReader))
                        {
                            var serializer = new JsonSerializer();
                            var userData = serializer.Deserialize<PercentageModel>(jsonReader);
                            return userData;
                        }
                    }
                }
                else
                {
                    // Handle unsuccessful response
                    Console.WriteLine($"Failed to fetch user data. Status code: {response.StatusCode}");
                }
            }
            catch (Exception ex)
            {
                // Handle exceptions
                Console.WriteLine($"An error occurred: {ex.Message}");
            }

            return null;
        }


    }

}