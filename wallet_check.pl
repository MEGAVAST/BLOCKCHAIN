#!/usr/bin/perl
use CGI;
#use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
$query = new CGI;
#use List::Uniq ':all';
#use CGI qw/:standard/; 
#use JSON;  # Imports the JSON module

$path="/home/dev2/Desktop/project_mini";
$log_file="wallet_status.log";
$wallets_list_file_name="$path/wallets_list.txt";

##### bcnt.io - system to send notifications to project - 
#------ V7 17.1.24 - testing data log files


read_wallet_list(); 

#test_wallet_details(); # load test parameters


sub read_wallet_list {   ### read the wallets_list and run the sys

    ## blockchain| wallet_id |token_id | wallet name | alert of token change ?(number) |
    ## POLYGON|0xC2661550B7c7b669f0034fE59895eFe5487673C2|0x689f8e5913c158ffb5ac5aeb83b3c875f5d20309|bcnt_wallet_test|500|


    open my $fh, '<', $wallets_list_file_name or die "Cannot open file: $!";

    while (my $line = <$fh>) {
        chomp $line;  # Remove the newline character at the end of the line

        # Split the line into components
        my @fields = split /\|/, $line;  ##/#

        # Check if all necessary fields are present
        unless (@fields >= 5) {
            warn "Incomplete data: $line\n";
            next;  # Skip this iteration if the data is incomplete
        }

        # Assign variables to each field
        ($blockchain, $wallet_id, $token_id, $wallet_name, $alert_threshold) = @fields;

        # Clean up fields
        $wallet_id =~ s/ //g;  # Remove spaces from $wallet_id

        # Output results
        print "Blockchain: $blockchain\n Wallet ID: $wallet_id\n Token ID: $token_id\n Wallet Name: $wallet_name\n Alert Threshold: $alert_threshold\n";





        check_wallet_status();
        get_json();
        compare_wallet_value();

        write_log();
        write_db();
        print_result();
    }

    close $fh; 
}


sub test_wallet_details {         ### parameters for test

    $blockchain="POLYGON";
    $wallet_id="0xC2661550B7c7b669f0034fE59895eFe5487673C2"; ##  0xe9b14a1Be94E70900EDdF1E22A4cB8c56aC9e10a";
    $token_id="0x689f8e5913c158ffb5ac5aeb83b3c875f5d20309"; ### snook token
    $wallet_name="bcnt_wallet_test";  ## waller owner name

}


sub check_wallet_status {        ### get the token status from the get_wallet2 
    ### https://bcnt.io/cgi-bin/CRYPTO/get_wallet2.py?wallet=0xe9b14a1Be94E70900EDdF1E22A4cB8c56aC9e10a&token=0x689f8e5913c158ffb5ac5aeb83b3c875f5d20309&block=POLYGON

    $blockchain;
    $wallet_id;
    $token_id;

    $wallet_status_json=`curl -s 'https://bcnt.io/cgi-bin/CRYPTO/get_wallet2.py?wallet=$wallet_id&token=$token_id&block=$blockchain'`;
}

sub get_json {                   # Decode JSON to Perl data structure
 
    if ($wallet_status_json =~ /"POLYGON":\s*\{"status":\s*"([^"]*)",\s*"balance":\s*"([^"]*)"\}/) {
        $status = $1;
        $balance = $2;   $balance = $balance / 1000000000000000000;  $balance= sprintf("%.2f", $balance);
    }
}

sub compare_wallet_value {       ### compare wallet value - open WALLETS_DB and check what was chaned

    $db_file_path = "$path/WALLET_DB/$wallet_id"; 

    unless (-e $db_file_path) { print "file problem"; exit; }  # Exit the subroutine if file doesn't exist

    # Open the file (ensure the file path is correct)
    $tail_file=`tail -1 $db_file_path | grep "$token_id" |cut -d"|" -f6 |cut -d":" -f2`;
    chomp $tail_file;

    $changed= $tail_file - $balance;     # Calculate the change in balance


    print "### - $tail_file\n";


}


sub print_result {

    #print "$wallet_status_json \n";
    print "$wallet_name Status: $status  Balance: $balance Changed: $changed \n  "
}

sub write_log {                    ### write log wallet_status.log

    open(GREP, ">>$path/$log_file");   
        $date2=`date`; chomp $date2;
        print GREP "$date2|$blockchain|$wallet_id|$token_id|$status|Balance: $balance|$changed|$token_usdt|$wallet_name|\n";
    close GREP;
}

sub write_db {                    ## write into DB directory
    $path;
    
    open(GREP, ">>$path/WALLET_DB/$wallet_id");   
        $date2=`date`; chomp $date2;
        print GREP "$date2|$blockchain|$wallet_id|$token_id|$status|Balance: $balance|$changed|$token_usdt|$wallet_name|\n";
    close GREP;


}

1;
