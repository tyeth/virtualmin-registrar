#!/usr/local/bin/perl
# Show a list of registered domains accessible to the current user

require 'virtualmin-registrar-lib.pl';
&ui_print_header(undef, $text{'list_title'}, "");
&ReadParse();

# Find the domains
@doms = grep { $_->{$module_name} &&
	       &virtual_server::can_edit_domain($_) }
	     &virtual_server::list_domains();

# Get relevant accounts
@accounts = &list_registrar_accounts();
if ($in{'id'}) {
	# Just one account
	@accounts = grep { $_->{'id'} eq $in{'id'} } @accounts;
	}

# Show each domain, with registration info
@table = ( );
foreach $d (@doms) {
	$url = &virtual_server::can_config_domain($d) ?
		"../virtual-server/edit_domain.cgi?id=$d->{'id'}" :
		"../virtual-server/view_domain.cgi?id=$d->{'id'}";
	($account) = grep { $_->{'id'} eq $d->{'registrar_account'} }
			  @accounts;
	next if (!$account);
	$rfunc = "type_".$account->{'registrar'}."_desc";
	$dname = &virtual_server::show_domain_name($d);

	# Get expiry date, if possible
	$efunc = "type_".$account->{'registrar'}."_get_expiry";
	$expiry = undef;
	if (defined(&$efunc)) {
		($ok, $expiry) = &$efunc($account, $d);
		$expiry = undef if (!$ok);
		}
	push(@table, [
		"<a href='$url'>$dname</a>",
		$account ? ( &$rfunc($account),
			     $account->{'desc'} )
			 : ( "None", "None" ),
		$d->{'registrar_id'},
		$expiry ? &make_date($expiry, 1) : undef,
		]);
	}
print &ui_columns_table(
	[ $text{'list_dom'}, $text{'list_registrar'},
	  $text{'list_account'}, $text{'list_id'},
	  $text{'list_expiry'}, ],
	100, \@table, undef, 0, undef, $text{'list_none'});

&ui_print_footer("/", $text{'index'});
