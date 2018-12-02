var months = ['01-Dec-13', '02-Dec-13', '03-Dec-13', '04-Dec-13', '05-Dec-13', '06-Dec-13', '07-Dec-13', '08-Dec-13', '09-Dec-13', '10-Dec-13', '11-Dec-13', '12-Dec-13', '13-Dec-13', '14-Dec-13', '15-Dec-13', '16-Dec-13', '17-Dec-13', '18-Dec-13', '19-Dec-13', '20-Dec-13', '21-Dec-13', '22-Dec-13', '23-Dec-13', '24-Dec-13', '25-Dec-13', '26-Dec-13', '27-Dec-13', '28-Dec-13', '29-Dec-13', '30-Dec-13', '31-Dec-13', '01-Jan-14', '02-Jan-14', '03-Jan-14', '04-Jan-14', '05-Jan-14', '06-Jan-14', '07-Jan-14', '08-Jan-14', '09-Jan-14', '10-Jan-14', '11-Jan-14', '12-Jan-14', '13-Jan-14', '14-Jan-14', '15-Jan-14', '16-Jan-14', '17-Jan-14', '18-Jan-14', '19-Jan-14', '20-Jan-14', '21-Jan-14', '22-Jan-14', '23-Jan-14', '24-Jan-14', '25-Jan-14', '26-Jan-14', '27-Jan-14', '28-Jan-14', '29-Jan-14', '30-Jan-14', '31-Jan-14', '01-Feb-14', '02-Feb-14', '03-Feb-14', '04-Feb-14', '05-Feb-14', '06-Feb-14', '07-Feb-14', '08-Feb-14', '09-Feb-14', '10-Feb-14', '11-Feb-14', '12-Feb-14', '13-Feb-14', '14-Feb-14', '15-Feb-14', '16-Feb-14', '17-Feb-14', '18-Feb-14', '19-Feb-14', '20-Feb-14', '21-Feb-14', '22-Feb-14', '23-Feb-14', '24-Feb-14', '25-Feb-14', '26-Feb-14', '27-Feb-14', '28-Feb-14', '01-Mar-14', '02-Mar-14', '03-Mar-14', '04-Mar-14', '05-Mar-14', '06-Mar-14', '07-Mar-14', '08-Mar-14', '09-Mar-14', '10-Mar-14', '11-Mar-14', '12-Mar-14', '13-Mar-14', '14-Mar-14', '15-Mar-14', '16-Mar-14', '17-Mar-14', '18-Mar-14', '19-Mar-14', '20-Mar-14', '21-Mar-14', '22-Mar-14', '23-Mar-14', '24-Mar-14', '25-Mar-14', '26-Mar-14', '27-Mar-14', '28-Mar-14', '29-Mar-14', '30-Mar-14', '31-Mar-14', '01-Apr-14', '02-Apr-14', '03-Apr-14', '04-Apr-14', '05-Apr-14', '06-Apr-14', '07-Apr-14', '08-Apr-14', '09-Apr-14', '10-Apr-14', '11-Apr-14', '12-Apr-14', '13-Apr-14', '14-Apr-14', '15-Apr-14', '16-Apr-14', '17-Apr-14', '18-Apr-14', '19-Apr-14', '20-Apr-14', '21-Apr-14', '22-Apr-14', '23-Apr-14', '24-Apr-14', '25-Apr-14', '26-Apr-14', '27-Apr-14', '28-Apr-14', '29-Apr-14', '30-Apr-14', '01-May-14', '02-May-14', '03-May-14', '04-May-14', '05-May-14', '06-May-14', '07-May-14', '08-May-14', '09-May-14', '10-May-14', '11-May-14', '12-May-14', '13-May-14', '14-May-14', '15-May-14', '16-May-14', '17-May-14', '18-May-14', '19-May-14', '20-May-14', '21-May-14', '22-May-14', '23-May-14', '24-May-14', '25-May-14', '26-May-14', '27-May-14', '28-May-14', '29-May-14', '30-May-14', '31-May-14', '01-Jun-14', '02-Jun-14', '03-Jun-14', '04-Jun-14', '05-Jun-14', '06-Jun-14', '07-Jun-14', '08-Jun-14', '09-Jun-14', '10-Jun-14', '11-Jun-14', '12-Jun-14', '13-Jun-14', '14-Jun-14', '15-Jun-14', '16-Jun-14', '17-Jun-14', '18-Jun-14', '19-Jun-14', '20-Jun-14', '21-Jun-14', '22-Jun-14', '23-Jun-14', '24-Jun-14', '25-Jun-14', '26-Jun-14', '27-Jun-14', '28-Jun-14', '29-Jun-14', '30-Jun-14', '01-Jul-14', '02-Jul-14', '03-Jul-14', '04-Jul-14', '05-Jul-14', '06-Jul-14', '07-Jul-14', '08-Jul-14', '09-Jul-14', '10-Jul-14', '11-Jul-14', '12-Jul-14', '13-Jul-14', '14-Jul-14', '15-Jul-14', '16-Jul-14', '17-Jul-14', '18-Jul-14', '19-Jul-14', '20-Jul-14', '21-Jul-14', '22-Jul-14', '23-Jul-14', '24-Jul-14', '25-Jul-14', '26-Jul-14', '27-Jul-14', '28-Jul-14', '29-Jul-14', '30-Jul-14', '31-Jul-14', '01-Aug-14', '02-Aug-14', '03-Aug-14', '04-Aug-14', '05-Aug-14', '06-Aug-14', '07-Aug-14', '08-Aug-14', '09-Aug-14', '10-Aug-14', '11-Aug-14', '12-Aug-14', '13-Aug-14', '14-Aug-14', '15-Aug-14', '16-Aug-14', '17-Aug-14', '18-Aug-14', '19-Aug-14', '20-Aug-14', '21-Aug-14', '22-Aug-14', '23-Aug-14', '24-Aug-14', '25-Aug-14', '26-Aug-14', '27-Aug-14', '28-Aug-14', '29-Aug-14', '30-Aug-14', '31-Aug-14', '01-Sep-14', '02-Sep-14', '03-Sep-14', '04-Sep-14', '05-Sep-14', '06-Sep-14', '07-Sep-14', '08-Sep-14', '09-Sep-14', '10-Sep-14', '11-Sep-14', '12-Sep-14', '13-Sep-14', '14-Sep-14', '15-Sep-14', '16-Sep-14', '17-Sep-14', '18-Sep-14', '19-Sep-14', '20-Sep-14', '21-Sep-14', '22-Sep-14', '23-Sep-14', '24-Sep-14', '25-Sep-14', '26-Sep-14', '27-Sep-14', '28-Sep-14', '29-Sep-14', '30-Sep-14', '01-Oct-14', '02-Oct-14', '03-Oct-14', '04-Oct-14', '05-Oct-14', '06-Oct-14', '07-Oct-14', '08-Oct-14', '09-Oct-14', '10-Oct-14', '11-Oct-14', '12-Oct-14', '13-Oct-14', '14-Oct-14', '15-Oct-14', '16-Oct-14', '17-Oct-14', '18-Oct-14', '19-Oct-14', '20-Oct-14', '21-Oct-14', '22-Oct-14', '23-Oct-14', '24-Oct-14', '25-Oct-14', '26-Oct-14', '27-Oct-14', '28-Oct-14', '29-Oct-14', '30-Oct-14', '31-Oct-14', '01-Nov-14', '02-Nov-14', '03-Nov-14', '04-Nov-14', '05-Nov-14', '06-Nov-14', '07-Nov-14', '08-Nov-14', '09-Nov-14', '10-Nov-14', '11-Nov-14', '12-Nov-14', '13-Nov-14', '14-Nov-14', '15-Nov-14', '16-Nov-14', '17-Nov-14', '18-Nov-14', '19-Nov-14', '20-Nov-14', '21-Nov-14', '22-Nov-14', '23-Nov-14', '24-Nov-14', '25-Nov-14', '26-Nov-14', '27-Nov-14', '28-Nov-14', '29-Nov-14', '30-Nov-14', '01-Dec-14', '02-Dec-14', '03-Dec-14', '04-Dec-14', '05-Dec-14', '06-Dec-14', '07-Dec-14', '08-Dec-14', '09-Dec-14', '10-Dec-14', '11-Dec-14', '12-Dec-14', '13-Dec-14', '14-Dec-14', '15-Dec-14', '16-Dec-14', '17-Dec-14', '18-Dec-14', '19-Dec-14', '20-Dec-14', '21-Dec-14', '22-Dec-14', '23-Dec-14', '24-Dec-14', '25-Dec-14', '26-Dec-14', '27-Dec-14', '28-Dec-14', '29-Dec-14', '30-Dec-14', '31-Dec-14', '01-Jan-15', '02-Jan-15', '03-Jan-15', '04-Jan-15', '05-Jan-15', '06-Jan-15', '07-Jan-15', '08-Jan-15', '09-Jan-15', '10-Jan-15', '11-Jan-15', '12-Jan-15', '13-Jan-15', '14-Jan-15', '15-Jan-15', '16-Jan-15', '17-Jan-15', '18-Jan-15', '19-Jan-15', '20-Jan-15', '21-Jan-15', '22-Jan-15', '23-Jan-15', '24-Jan-15', '25-Jan-15', '26-Jan-15', '27-Jan-15', '28-Jan-15', '29-Jan-15', '30-Jan-15', '31-Jan-15', '01-Feb-15', '02-Feb-15', '03-Feb-15', '04-Feb-15', '05-Feb-15', '06-Feb-15', '07-Feb-15', '08-Feb-15', '09-Feb-15', '10-Feb-15', '11-Feb-15', '12-Feb-15', '13-Feb-15', '14-Feb-15', '15-Feb-15', '16-Feb-15', '17-Feb-15', '18-Feb-15', '19-Feb-15', '20-Feb-15', '21-Feb-15', '22-Feb-15', '23-Feb-15', '24-Feb-15', '25-Feb-15', '26-Feb-15', '27-Feb-15', '28-Feb-15', '01-Mar-15', '02-Mar-15', '03-Mar-15', '04-Mar-15', '05-Mar-15', '06-Mar-15', '07-Mar-15', '08-Mar-15', '09-Mar-15', '10-Mar-15', '11-Mar-15', '12-Mar-15', '13-Mar-15', '14-Mar-15', '15-Mar-15', '16-Mar-15', '17-Mar-15', '18-Mar-15', '19-Mar-15', '20-Mar-15', '21-Mar-15', '22-Mar-15', '23-Mar-15', '24-Mar-15', '25-Mar-15', '26-Mar-15', '27-Mar-15', '28-Mar-15', '29-Mar-15', '30-Mar-15', '31-Mar-15', '01-Apr-15', '02-Apr-15', '03-Apr-15', '04-Apr-15', '05-Apr-15', '06-Apr-15', '07-Apr-15', '08-Apr-15', '09-Apr-15', '10-Apr-15', '11-Apr-15', '12-Apr-15', '13-Apr-15', '14-Apr-15', '15-Apr-15', '16-Apr-15', '17-Apr-15', '18-Apr-15', '19-Apr-15', '20-Apr-15', '21-Apr-15', '22-Apr-15', '23-Apr-15', '24-Apr-15', '25-Apr-15', '26-Apr-15', '27-Apr-15', '28-Apr-15', '29-Apr-15', '30-Apr-15', '01-May-15', '02-May-15', '03-May-15', '04-May-15', '05-May-15', '06-May-15', '07-May-15', '08-May-15', '09-May-15', '10-May-15', '11-May-15', '12-May-15', '13-May-15', '14-May-15', '15-May-15', '16-May-15', '17-May-15', '18-May-15', '19-May-15', '20-May-15', '21-May-15', '22-May-15', '23-May-15', '24-May-15', '25-May-15', '26-May-15', '27-May-15', '28-May-15', '29-May-15', '30-May-15', '31-May-15', '01-Jun-15', '02-Jun-15', '03-Jun-15', '04-Jun-15', '05-Jun-15', '06-Jun-15', '07-Jun-15', '08-Jun-15', '09-Jun-15', '10-Jun-15', '11-Jun-15', '12-Jun-15', '13-Jun-15', '14-Jun-15', '15-Jun-15', '16-Jun-15', '17-Jun-15', '18-Jun-15', '19-Jun-15', '20-Jun-15', '21-Jun-15', '22-Jun-15', '23-Jun-15', '24-Jun-15', '25-Jun-15', '26-Jun-15', '27-Jun-15', '28-Jun-15', '29-Jun-15', '30-Jun-15', '01-Jul-15', '02-Jul-15', '03-Jul-15', '04-Jul-15', '05-Jul-15', '06-Jul-15', '07-Jul-15', '08-Jul-15', '09-Jul-15', '10-Jul-15', '11-Jul-15', '12-Jul-15', '13-Jul-15', '14-Jul-15', '15-Jul-15', '16-Jul-15', '17-Jul-15', '18-Jul-15', '19-Jul-15', '20-Jul-15', '21-Jul-15', '22-Jul-15', '23-Jul-15', '24-Jul-15', '25-Jul-15', '26-Jul-15', '27-Jul-15', '28-Jul-15', '29-Jul-15', '30-Jul-15', '31-Jul-15', '01-Aug-15', '02-Aug-15', '03-Aug-15', '04-Aug-15', '05-Aug-15', '06-Aug-15', '07-Aug-15', '08-Aug-15', '09-Aug-15', '10-Aug-15', '11-Aug-15', '12-Aug-15', '13-Aug-15', '14-Aug-15', '15-Aug-15', '16-Aug-15', '17-Aug-15', '18-Aug-15', '19-Aug-15', '20-Aug-15', '21-Aug-15', '22-Aug-15', '23-Aug-15', '24-Aug-15', '25-Aug-15', '26-Aug-15', '27-Aug-15', '28-Aug-15', '29-Aug-15', '30-Aug-15', '31-Aug-15', '01-Sep-15', '02-Sep-15', '03-Sep-15', '04-Sep-15', '05-Sep-15', '06-Sep-15', '07-Sep-15', '08-Sep-15', '09-Sep-15', '10-Sep-15', '11-Sep-15', '12-Sep-15', '13-Sep-15', '14-Sep-15', '15-Sep-15', '16-Sep-15', '17-Sep-15', '18-Sep-15', '19-Sep-15', '20-Sep-15', '21-Sep-15', '22-Sep-15', '23-Sep-15', '24-Sep-15', '25-Sep-15', '26-Sep-15', '27-Sep-15', '28-Sep-15', '29-Sep-15', '30-Sep-15', '01-Oct-15', '02-Oct-15', '03-Oct-15', '04-Oct-15', '05-Oct-15', '06-Oct-15', '07-Oct-15', '08-Oct-15', '09-Oct-15', '10-Oct-15', '11-Oct-15', '12-Oct-15', '13-Oct-15', '14-Oct-15', '15-Oct-15', '16-Oct-15', '17-Oct-15', '18-Oct-15', '19-Oct-15', '20-Oct-15', '21-Oct-15', '22-Oct-15', '23-Oct-15', '24-Oct-15', '25-Oct-15', '26-Oct-15', '27-Oct-15', '28-Oct-15', '29-Oct-15', '30-Oct-15', '31-Oct-15', '01-Nov-15', '02-Nov-15', '03-Nov-15', '04-Nov-15', '05-Nov-15', '06-Nov-15', '07-Nov-15', '08-Nov-15', '09-Nov-15', '10-Nov-15', '11-Nov-15', '12-Nov-15', '13-Nov-15', '14-Nov-15', '15-Nov-15', '16-Nov-15', '17-Nov-15', '18-Nov-15', '19-Nov-15', '20-Nov-15', '21-Nov-15', '22-Nov-15', '23-Nov-15', '24-Nov-15', '25-Nov-15', '26-Nov-15', '27-Nov-15', '28-Nov-15', '29-Nov-15', '30-Nov-15', '01-Dec-15', '02-Dec-15', '03-Dec-15', '04-Dec-15', '05-Dec-15', '06-Dec-15', '07-Dec-15', '08-Dec-15', '09-Dec-15', '10-Dec-15', '11-Dec-15', '12-Dec-15', '13-Dec-15', '14-Dec-15', '15-Dec-15', '16-Dec-15', '17-Dec-15', '18-Dec-15', '19-Dec-15', '20-Dec-15', '21-Dec-15', '22-Dec-15', '23-Dec-15', '24-Dec-15', '25-Dec-15', '26-Dec-15', '27-Dec-15', '28-Dec-15', '29-Dec-15', '30-Dec-15', '31-Dec-15', '01-Jan-16', '02-Jan-16', '03-Jan-16', '04-Jan-16', '05-Jan-16', '06-Jan-16', '07-Jan-16', '08-Jan-16', '09-Jan-16', '10-Jan-16', '11-Jan-16', '12-Jan-16', '13-Jan-16', '14-Jan-16', '15-Jan-16', '16-Jan-16', '17-Jan-16', '18-Jan-16', '19-Jan-16', '20-Jan-16', '21-Jan-16', '22-Jan-16', '23-Jan-16', '24-Jan-16', '25-Jan-16', '26-Jan-16', '27-Jan-16', '28-Jan-16', '29-Jan-16', '30-Jan-16', '31-Jan-16', '01-Feb-16', '02-Feb-16', '03-Feb-16', '04-Feb-16', '05-Feb-16', '06-Feb-16', '07-Feb-16', '08-Feb-16', '09-Feb-16', '10-Feb-16', '11-Feb-16', '12-Feb-16', '13-Feb-16', '14-Feb-16', '15-Feb-16', '16-Feb-16', '17-Feb-16', '18-Feb-16', '19-Feb-16', '20-Feb-16', '21-Feb-16', '22-Feb-16', '23-Feb-16', '24-Feb-16', '25-Feb-16', '26-Feb-16', '27-Feb-16', '28-Feb-16', '29-Feb-16', '01-Mar-16', '02-Mar-16', '03-Mar-16', '04-Mar-16', '05-Mar-16', '06-Mar-16', '07-Mar-16', '08-Mar-16', '09-Mar-16', '10-Mar-16', '11-Mar-16', '12-Mar-16', '13-Mar-16', '14-Mar-16', '15-Mar-16', '16-Mar-16', '17-Mar-16', '18-Mar-16', '19-Mar-16', '20-Mar-16', '21-Mar-16', '22-Mar-16', '23-Mar-16', '24-Mar-16', '25-Mar-16', '26-Mar-16', '27-Mar-16', '28-Mar-16', '29-Mar-16', '30-Mar-16', '31-Mar-16', '01-Apr-16', '02-Apr-16', '03-Apr-16', '04-Apr-16', '05-Apr-16', '06-Apr-16', '07-Apr-16', '08-Apr-16', '09-Apr-16', '10-Apr-16', '11-Apr-16', '12-Apr-16', '13-Apr-16', '14-Apr-16', '15-Apr-16', '16-Apr-16', '17-Apr-16', '18-Apr-16', '19-Apr-16', '20-Apr-16', '21-Apr-16', '22-Apr-16', '23-Apr-16', '24-Apr-16', '25-Apr-16', '26-Apr-16', '27-Apr-16', '28-Apr-16', '29-Apr-16', '30-Apr-16', '01-May-16', '02-May-16', '03-May-16', '04-May-16', '05-May-16', '06-May-16', '07-May-16', '08-May-16', '09-May-16', '10-May-16', '11-May-16', '12-May-16', '13-May-16', '14-May-16', '15-May-16', '16-May-16', '17-May-16', '18-May-16', '19-May-16', '20-May-16', '21-May-16', '22-May-16', '23-May-16', '24-May-16', '25-May-16', '26-May-16', '27-May-16', '28-May-16', '29-May-16', '30-May-16', '31-May-16', '01-Jun-16', '02-Jun-16', '03-Jun-16', '04-Jun-16', '05-Jun-16', '06-Jun-16', '07-Jun-16', '08-Jun-16', '09-Jun-16', '10-Jun-16', '11-Jun-16', '12-Jun-16', '13-Jun-16', '14-Jun-16', '15-Jun-16', '16-Jun-16', '17-Jun-16', '18-Jun-16', '19-Jun-16', '20-Jun-16', '21-Jun-16', '22-Jun-16', '23-Jun-16', '24-Jun-16', '25-Jun-16', '26-Jun-16', '27-Jun-16', '28-Jun-16', '29-Jun-16', '30-Jun-16', '01-Jul-16', '02-Jul-16', '03-Jul-16', '04-Jul-16', '05-Jul-16', '06-Jul-16', '07-Jul-16', '08-Jul-16', '09-Jul-16', '10-Jul-16', '11-Jul-16', '12-Jul-16', '13-Jul-16', '14-Jul-16', '15-Jul-16', '16-Jul-16', '17-Jul-16', '18-Jul-16', '19-Jul-16', '20-Jul-16', '21-Jul-16', '22-Jul-16', '23-Jul-16', '24-Jul-16', '25-Jul-16', '26-Jul-16', '27-Jul-16', '28-Jul-16', '29-Jul-16', '30-Jul-16', '31-Jul-16', '01-Aug-16', '02-Aug-16', '03-Aug-16', '04-Aug-16', '05-Aug-16', '06-Aug-16', '07-Aug-16', '08-Aug-16', '09-Aug-16', '10-Aug-16', '11-Aug-16', '12-Aug-16', '13-Aug-16', '14-Aug-16', '15-Aug-16', '16-Aug-16', '17-Aug-16', '18-Aug-16', '19-Aug-16', '20-Aug-16', '21-Aug-16', '22-Aug-16', '23-Aug-16', '24-Aug-16', '25-Aug-16', '26-Aug-16', '27-Aug-16', '28-Aug-16', '29-Aug-16', '30-Aug-16', '31-Aug-16', '01-Sep-16', '02-Sep-16', '03-Sep-16', '04-Sep-16', '05-Sep-16', '06-Sep-16', '07-Sep-16', '08-Sep-16', '09-Sep-16', '10-Sep-16', '11-Sep-16', '12-Sep-16', '13-Sep-16', '14-Sep-16', '15-Sep-16', '16-Sep-16', '17-Sep-16', '18-Sep-16', '19-Sep-16', '20-Sep-16', '21-Sep-16', '22-Sep-16', '23-Sep-16', '24-Sep-16', '25-Sep-16', '26-Sep-16', '27-Sep-16', '28-Sep-16', '29-Sep-16', '30-Sep-16', '01-Oct-16', '02-Oct-16', '03-Oct-16', '04-Oct-16', '05-Oct-16', '06-Oct-16', '07-Oct-16', '08-Oct-16', '09-Oct-16', '10-Oct-16', '11-Oct-16', '12-Oct-16', '13-Oct-16', '14-Oct-16', '15-Oct-16', '16-Oct-16', '17-Oct-16', '18-Oct-16', '19-Oct-16', '20-Oct-16', '21-Oct-16', '22-Oct-16', '23-Oct-16', '24-Oct-16', '25-Oct-16', '26-Oct-16', '27-Oct-16', '28-Oct-16', '29-Oct-16', '30-Oct-16', '31-Oct-16', '01-Nov-16', '02-Nov-16', '03-Nov-16', '04-Nov-16', '05-Nov-16', '06-Nov-16', '07-Nov-16', '08-Nov-16', '09-Nov-16', '10-Nov-16', '11-Nov-16', '12-Nov-16', '13-Nov-16', '14-Nov-16', '15-Nov-16', '16-Nov-16', '17-Nov-16', '18-Nov-16', '19-Nov-16', '20-Nov-16', '21-Nov-16', '22-Nov-16', '23-Nov-16', '24-Nov-16', '25-Nov-16', '26-Nov-16', '27-Nov-16', '28-Nov-16', '29-Nov-16', '30-Nov-16', '01-Dec-16', '02-Dec-16', '03-Dec-16', '04-Dec-16', '05-Dec-16', '06-Dec-16', '07-Dec-16', '08-Dec-16', '09-Dec-16', '10-Dec-16', '11-Dec-16', '12-Dec-16', '13-Dec-16', '14-Dec-16', '15-Dec-16', '16-Dec-16', '17-Dec-16', '18-Dec-16', '19-Dec-16', '20-Dec-16', '21-Dec-16', '22-Dec-16', '23-Dec-16', '24-Dec-16', '25-Dec-16', '26-Dec-16', '27-Dec-16', '28-Dec-16', '29-Dec-16', '30-Dec-16', '31-Dec-16', '01-Jan-17', '02-Jan-17', '03-Jan-17', '04-Jan-17', '05-Jan-17', '06-Jan-17', '07-Jan-17', '08-Jan-17', '09-Jan-17', '10-Jan-17', '11-Jan-17', '12-Jan-17', '13-Jan-17', '14-Jan-17', '15-Jan-17', '16-Jan-17', '17-Jan-17', '18-Jan-17', '19-Jan-17', '20-Jan-17', '21-Jan-17', '22-Jan-17', '23-Jan-17', '24-Jan-17', '25-Jan-17', '26-Jan-17', '27-Jan-17', '28-Jan-17', '29-Jan-17', '30-Jan-17', '31-Jan-17', '01-Feb-17', '02-Feb-17', '03-Feb-17', '04-Feb-17', '05-Feb-17', '06-Feb-17', '07-Feb-17', '08-Feb-17', '09-Feb-17', '10-Feb-17', '11-Feb-17', '12-Feb-17', '13-Feb-17', '14-Feb-17', '15-Feb-17', '16-Feb-17', '17-Feb-17', '18-Feb-17', '19-Feb-17', '20-Feb-17', '21-Feb-17', '22-Feb-17', '23-Feb-17', '24-Feb-17', '25-Feb-17', '26-Feb-17', '27-Feb-17', '28-Feb-17', '01-Mar-17', '02-Mar-17', '03-Mar-17', '04-Mar-17', '05-Mar-17', '06-Mar-17', '07-Mar-17', '08-Mar-17', '09-Mar-17', '10-Mar-17', '11-Mar-17', '12-Mar-17', '13-Mar-17', '14-Mar-17', '15-Mar-17', '16-Mar-17', '17-Mar-17', '18-Mar-17', '19-Mar-17', '20-Mar-17', '21-Mar-17', '22-Mar-17', '23-Mar-17', '24-Mar-17', '25-Mar-17', '26-Mar-17', '27-Mar-17', '28-Mar-17', '29-Mar-17', '30-Mar-17', '31-Mar-17', '01-Apr-17', '02-Apr-17', '03-Apr-17', '04-Apr-17', '05-Apr-17', '06-Apr-17', '07-Apr-17', '08-Apr-17', '09-Apr-17', '10-Apr-17', '11-Apr-17', '12-Apr-17', '13-Apr-17', '14-Apr-17', '15-Apr-17', '16-Apr-17', '17-Apr-17', '18-Apr-17', '19-Apr-17', '20-Apr-17', '21-Apr-17', '22-Apr-17', '23-Apr-17', '24-Apr-17', '25-Apr-17', '26-Apr-17', '27-Apr-17', '28-Apr-17', '29-Apr-17', '30-Apr-17', '01-May-17', '02-May-17', '03-May-17', '04-May-17', '05-May-17', '06-May-17', '07-May-17', '08-May-17', '09-May-17', '10-May-17', '11-May-17', '12-May-17', '13-May-17', '14-May-17', '15-May-17', '16-May-17', '17-May-17', '18-May-17', '19-May-17', '20-May-17', '21-May-17', '22-May-17', '23-May-17', '24-May-17', '25-May-17', '26-May-17', '27-May-17', '28-May-17', '29-May-17', '30-May-17', '31-May-17', '01-Jun-17', '02-Jun-17', '03-Jun-17', '04-Jun-17', '05-Jun-17', '06-Jun-17', '07-Jun-17', '08-Jun-17', '09-Jun-17', '10-Jun-17', '11-Jun-17', '12-Jun-17', '13-Jun-17', '14-Jun-17', '15-Jun-17', '16-Jun-17', '17-Jun-17', '18-Jun-17', '19-Jun-17', '20-Jun-17', '21-Jun-17', '22-Jun-17', '23-Jun-17', '24-Jun-17', '25-Jun-17', '26-Jun-17', '27-Jun-17', '28-Jun-17', '29-Jun-17', '30-Jun-17', '01-Jul-17', '02-Jul-17', '03-Jul-17', '04-Jul-17', '05-Jul-17', '06-Jul-17', '07-Jul-17', '08-Jul-17', '09-Jul-17', '10-Jul-17', '11-Jul-17', '12-Jul-17', '13-Jul-17', '14-Jul-17', '15-Jul-17', '16-Jul-17', '17-Jul-17', '18-Jul-17', '19-Jul-17', '20-Jul-17', '21-Jul-17', '22-Jul-17', '23-Jul-17', '24-Jul-17', '25-Jul-17', '26-Jul-17', '27-Jul-17', '28-Jul-17', '29-Jul-17', '30-Jul-17', '31-Jul-17', '01-Aug-17', '02-Aug-17', '03-Aug-17', '04-Aug-17', '05-Aug-17', '06-Aug-17', '07-Aug-17', '08-Aug-17', '09-Aug-17', '10-Aug-17', '11-Aug-17', '12-Aug-17', '13-Aug-17', '14-Aug-17', '15-Aug-17', '16-Aug-17', '17-Aug-17', '18-Aug-17', '19-Aug-17', '20-Aug-17', '21-Aug-17', '22-Aug-17', '23-Aug-17', '24-Aug-17', '25-Aug-17', '26-Aug-17', '27-Aug-17', '28-Aug-17', '29-Aug-17', '30-Aug-17', '31-Aug-17', '01-Sep-17', '02-Sep-17', '03-Sep-17', '04-Sep-17', '05-Sep-17', '06-Sep-17', '07-Sep-17', '08-Sep-17', '09-Sep-17', '10-Sep-17', '11-Sep-17', '12-Sep-17', '13-Sep-17', '14-Sep-17', '15-Sep-17', '16-Sep-17', '17-Sep-17', '18-Sep-17', '19-Sep-17', '20-Sep-17', '21-Sep-17', '22-Sep-17', '23-Sep-17', '24-Sep-17', '25-Sep-17', '26-Sep-17', '27-Sep-17', '28-Sep-17', '29-Sep-17', '30-Sep-17', '01-Oct-17', '02-Oct-17', '03-Oct-17', '04-Oct-17', '05-Oct-17', '06-Oct-17', '07-Oct-17', '08-Oct-17', '09-Oct-17', '10-Oct-17', '11-Oct-17', '12-Oct-17', '13-Oct-17', '14-Oct-17', '15-Oct-17', '16-Oct-17', '17-Oct-17', '18-Oct-17', '19-Oct-17', '20-Oct-17', '21-Oct-17', '22-Oct-17', '23-Oct-17', '24-Oct-17', '25-Oct-17', '26-Oct-17', '27-Oct-17', '28-Oct-17', '29-Oct-17', '30-Oct-17', '31-Oct-17', '01-Nov-17', '02-Nov-17', '03-Nov-17', '04-Nov-17', '05-Nov-17', '06-Nov-17', '07-Nov-17', '08-Nov-17', '09-Nov-17', '10-Nov-17', '11-Nov-17', '12-Nov-17', '13-Nov-17', '14-Nov-17', '15-Nov-17', '16-Nov-17', '17-Nov-17', '18-Nov-17', '19-Nov-17', '20-Nov-17', '21-Nov-17', '22-Nov-17', '23-Nov-17', '24-Nov-17', '25-Nov-17', '26-Nov-17', '27-Nov-17', '28-Nov-17', '29-Nov-17', '30-Nov-17', '01-Dec-17', '02-Dec-17', '03-Dec-17', '04-Dec-17', '05-Dec-17', '06-Dec-17', '07-Dec-17', '08-Dec-17', '09-Dec-17', '10-Dec-17', '11-Dec-17', '12-Dec-17', '13-Dec-17', '14-Dec-17', '15-Dec-17', '16-Dec-17', '17-Dec-17', '18-Dec-17', '19-Dec-17', '20-Dec-17', '21-Dec-17', '22-Dec-17', '23-Dec-17', '24-Dec-17', '25-Dec-17', '26-Dec-17', '27-Dec-17', '28-Dec-17', '29-Dec-17', '30-Dec-17', '31-Dec-17', '01-Jan-18', '02-Jan-18', '03-Jan-18', '04-Jan-18', '05-Jan-18', '06-Jan-18', '07-Jan-18', '08-Jan-18', '09-Jan-18', '10-Jan-18', '11-Jan-18', '12-Jan-18', '13-Jan-18', '14-Jan-18', '15-Jan-18', '16-Jan-18', '17-Jan-18', '18-Jan-18', '19-Jan-18', '20-Jan-18', '21-Jan-18', '22-Jan-18', '23-Jan-18', '24-Jan-18', '25-Jan-18', '26-Jan-18', '27-Jan-18', '28-Jan-18', '29-Jan-18', '30-Jan-18', '31-Jan-18', '01-Feb-18', '02-Feb-18', '03-Feb-18', '04-Feb-18', '05-Feb-18', '06-Feb-18', '07-Feb-18', '08-Feb-18', '09-Feb-18', '10-Feb-18', '11-Feb-18', '12-Feb-18', '13-Feb-18', '14-Feb-18', '15-Feb-18', '16-Feb-18', '17-Feb-18', '18-Feb-18', '19-Feb-18', '20-Feb-18', '21-Feb-18', '22-Feb-18', '23-Feb-18', '24-Feb-18', '25-Feb-18', '26-Feb-18', '27-Feb-18', '28-Feb-18', '01-Mar-18', '02-Mar-18', '03-Mar-18', '04-Mar-18', '05-Mar-18', '06-Mar-18', '07-Mar-18', '08-Mar-18', '09-Mar-18', '10-Mar-18', '11-Mar-18', '12-Mar-18', '13-Mar-18', '14-Mar-18', '15-Mar-18', '16-Mar-18', '17-Mar-18', '18-Mar-18', '19-Mar-18', '20-Mar-18', '21-Mar-18', '22-Mar-18', '23-Mar-18', '24-Mar-18', '25-Mar-18', '26-Mar-18', '27-Mar-18', '28-Mar-18', '29-Mar-18', '30-Mar-18', '31-Mar-18', '01-Apr-18', '02-Apr-18', '03-Apr-18', '04-Apr-18', '05-Apr-18', '06-Apr-18', '07-Apr-18', '08-Apr-18', '09-Apr-18', '10-Apr-18', '11-Apr-18', '12-Apr-18', '13-Apr-18', '14-Apr-18', '15-Apr-18', '16-Apr-18', '17-Apr-18', '18-Apr-18', '19-Apr-18', '20-Apr-18', '21-Apr-18', '22-Apr-18', '23-Apr-18', '24-Apr-18', '25-Apr-18', '26-Apr-18', '27-Apr-18', '28-Apr-18', '29-Apr-18', '30-Apr-18', '01-May-18', '02-May-18', '03-May-18', '04-May-18', '05-May-18', '06-May-18', '07-May-18', '08-May-18', '09-May-18', '10-May-18', '11-May-18', '12-May-18', '13-May-18', '14-May-18', '15-May-18', '16-May-18', '17-May-18', '18-May-18', '19-May-18', '20-May-18', '21-May-18', '22-May-18', '23-May-18', '24-May-18', '25-May-18', '26-May-18', '27-May-18', '28-May-18', '29-May-18', '30-May-18', '31-May-18', '01-Jun-18', '02-Jun-18', '03-Jun-18', '04-Jun-18', '05-Jun-18', '06-Jun-18', '07-Jun-18', '08-Jun-18', '09-Jun-18', '10-Jun-18', '11-Jun-18', '12-Jun-18', '13-Jun-18', '14-Jun-18', '15-Jun-18', '16-Jun-18', '17-Jun-18', '18-Jun-18', '19-Jun-18', '20-Jun-18', '21-Jun-18', '22-Jun-18', '23-Jun-18', '24-Jun-18', '25-Jun-18', '26-Jun-18', '27-Jun-18', '28-Jun-18', '29-Jun-18', '30-Jun-18', '01-Jul-18', '02-Jul-18', '03-Jul-18', '04-Jul-18', '05-Jul-18', '06-Jul-18', '07-Jul-18', '08-Jul-18', '09-Jul-18', '10-Jul-18', '11-Jul-18', '12-Jul-18', '13-Jul-18', '14-Jul-18', '15-Jul-18', '16-Jul-18', '17-Jul-18', '18-Jul-18', '19-Jul-18', '20-Jul-18', '21-Jul-18', '22-Jul-18', '23-Jul-18', '24-Jul-18', '25-Jul-18', '26-Jul-18', '27-Jul-18', '28-Jul-18', '29-Jul-18', '30-Jul-18', '31-Jul-18', '01-Aug-18', '02-Aug-18', '03-Aug-18', '04-Aug-18', '05-Aug-18', '06-Aug-18', '07-Aug-18', '08-Aug-18', '09-Aug-18', '10-Aug-18', '11-Aug-18', '12-Aug-18', '13-Aug-18', '14-Aug-18', '15-Aug-18', '16-Aug-18', '17-Aug-18', '18-Aug-18', '19-Aug-18', '20-Aug-18', '21-Aug-18', '22-Aug-18', '23-Aug-18', '24-Aug-18', '25-Aug-18', '26-Aug-18', '27-Aug-18', '28-Aug-18', '29-Aug-18', '30-Aug-18', '31-Aug-18', '01-Sep-18', '02-Sep-18', '03-Sep-18', '04-Sep-18', '05-Sep-18', '06-Sep-18', '07-Sep-18', '08-Sep-18', '09-Sep-18', '10-Sep-18', '11-Sep-18', '12-Sep-18', '13-Sep-18', '14-Sep-18', '15-Sep-18', '16-Sep-18', '17-Sep-18', '18-Sep-18', '19-Sep-18', '20-Sep-18', '21-Sep-18', '22-Sep-18', '23-Sep-18', '24-Sep-18', '25-Sep-18', '26-Sep-18', '27-Sep-18', '28-Sep-18', '29-Sep-18', '30-Sep-18', '01-Oct-18', '02-Oct-18', '03-Oct-18', '04-Oct-18', '05-Oct-18', '06-Oct-18', '07-Oct-18', '08-Oct-18', '09-Oct-18', '10-Oct-18', '11-Oct-18', '12-Oct-18', '13-Oct-18', '14-Oct-18', '15-Oct-18', '16-Oct-18', '17-Oct-18', '18-Oct-18', '19-Oct-18', '20-Oct-18', '21-Oct-18', '22-Oct-18', '23-Oct-18', '24-Oct-18', '25-Oct-18', '26-Oct-18', '27-Oct-18', '28-Oct-18', '29-Oct-18', '30-Oct-18', '31-Oct-18', '01-Nov-18', '02-Nov-18', '03-Nov-18', '04-Nov-18', '05-Nov-18', '06-Nov-18', '07-Nov-18', '08-Nov-18', '09-Nov-18', '10-Nov-18', '11-Nov-18', '12-Nov-18', '13-Nov-18', '14-Nov-18', '15-Nov-18', '16-Nov-18', '17-Nov-18', '18-Nov-18', '19-Nov-18', '20-Nov-18', '21-Nov-18', '22-Nov-18', '23-Nov-18', '24-Nov-18', '25-Nov-18', '26-Nov-18', '27-Nov-18', '28-Nov-18', '29-Nov-18', '30-Nov-18'];

//chart data stores data of our portfolio backtested, 
function generate_better(user_id){
    let better_portfolio = {};
    let chart_data;
    document.getElementsByClassName("tooltip-inner")[0].style.display = "None";
    $.getJSON('/api/back_test_user?user_id='+ user_id, 
        function(data) {
            chart_data = data;
        }).done(function() {$.getJSON('/api/improve_portfolio?user_id=' + user_id, 
            function(data){
                sharpe = data['sharpe_p'];
                return_val = data['return'];
                sigma = data['sigma'];
                //better stores the weights of our new assets
                for (let i = 0; i < data['ticker'].length; i++){
                    better_portfolio[data['ticker'][i]] = data['weights'][i];
                }
                let get_request = { 'tickers': data['ticker'], 'weights': data['weights']};
                $.getJSON('/api/back_test_portfolio', get_request, function(data) {
                    console.log(data);
                })
                display_both_portfolios(chart_data, better_portfolio, user_id);
            })
        })
};

function display_both_portfolios(chart_data, better, user_id) {
        let user_portfolio = {}
        $.getJSON('/api/portfolios?user_id=' + user_id, function(data){
            let new_amounts = data['amount'];
            new_tickers = data['ticker'];
            for (let i = 0; i < new_amounts.length; i++){
                user_portfolio[new_tickers[i]] = new_amounts[i];
            }
        }).done(function(){
        var table = "<div class = 'tablewrapper'><table class='table'><thead><tr><th scope='col'>Ticker</th><th scope='col'>Value per stock($USD)</th><th scope='col'>Amount in Your Portfolio</th><th scope='col'>Amount in generated</th></tr></thead><tbody id = 'bodytable'></tbody></table></div>";
        document.getElementById("card-page").innerHTML = "<div class=\"card border-primary mb-4 text-center hoverable\" style = \"width: 70%; margin: 0 auto; height: 50%;padding: 20px 0\"><canvas id = 'newCanvas'></canvas>"+ table;
        document.getElementById("card-page").setAttribute("style", "width: 95%; margin-bottom: 40px; background: transparent");
        document.getElementsByClassName("arrow")[0].style.display = "None";
        var ctx = document.getElementById("newCanvas");
        var table_data = '';
        for (ticker in better){
            let curr = "<tr>";
            curr +=  "<th scope='row'>"+ticker+"</th><td>$5 placeholder</td><td>"+user_portfolio[ticker]+"</td><td>"+better[ticker]+"</td></tr>";
            table_data += curr;
        }
        document.getElementById('bodytable').innerHTML = table_data;
        var display_data = [];
        for (var i = 0; i < months.length; i++){
            if (i % 7 == 0){
                display_data.push(months[i])
            }
        }
        while (display_data.length % 23 != 0) {
            display_data.shift();
            chart_data.shift();
        }
        ctx.style.backgroundColor = 'white';
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
            labels: display_data,
            datasets: [{ 
                lineTension: 0,
                data: chart_data,
                borderColor: "#3e95cd",
                fill: false,
                label: "Your Portfolio"
                }
            ]
            },
            options: {
                defaultFontSize: 14,
                
                scales: {
                    yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Value in $ (USD)',
                        fontSize: 16
                    }
                    
                    }],
                    xAxes: [{
                        scaleLabel: {
                          display: true,
                          labelString: 'Date: Day/Month/Year',
                          fontSize: 16
                        }
                      }] 
                    },
            title: {
                display: true,
                text: 'Value over time of your Portfolio versus our generated Portfolio',
                fontSize: 16
            }
            }
        });
    })
};

function backtest(user_id) {
    if (confirm("Are you sure you want to backtest?")){
        document.getElementsByClassName("tooltip-inner")[0].style.display = "None";
        document.getElementsByClassName("arrow")[0].style.display = "None";
        $.getJSON('/api/back_test_user?user_id='+ user_id, function(data) {
            chart_data = data;
        }).done(function() {
            document.getElementById("card-page").innerHTML = "<canvas id = 'myChart'></canvas>";
            var ctx = document.getElementById("myChart");
            var display_data = [];
            for (var i = 0; i < months.length; i++){
                if (i % 7 == 0){
                    display_data.push(months[i])
                }
            }
            while (display_data.length % 23 != 0) {
                display_data.shift();
                chart_data.shift();
            }
            ctx.style.backgroundColor = 'white';
            var myChart = new Chart(ctx, {
                type: 'line',
                data: {
                labels: display_data,
                datasets: [{ 
                    lineTension: 0,
                    data: chart_data,
                    borderColor: "#3e95cd",
                    fill: false,
                    label: "Portfolio"
                    }
                ]
                },
                options: {
                    defaultFontSize: 14,
                    
                    scales: {
                        yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: 'Value in $ (USD)',
                            fontSize: 16
                        }
                        
                        }],
                        xAxes: [{
                            scaleLabel: {
                              display: true,
                              labelString: 'Date: Day/Month/Year',
                              fontSize: 16
                            }
                          }] 
                        },
                title: {
                    display: true,
                    text: 'Value over time of Portfolio',
                    fontSize: 16
                }
                }
            });
        });
    };
}

