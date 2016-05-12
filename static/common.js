var title = '<title>CoCatalyst</title>';
var navigationbar = '<nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">'+
                        '<div class="container">'+
                        '<!-- Brand and toggle get grouped for better mobile display -->'+
                            '<div class="navbar-header">'+
                                '<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">'+
                                    '<span class="sr-only">Toggle navigation</span>'+
                                    '<span class="icon-bar"></span>'+
                                    '<span class="icon-bar"></span>'+
                                    '<span class="icon-bar"></span>'+
                                '</button>'+
                                '<a class="navbar-brand" href="/login">CoCatalyst</a>'+
                                '<!-- <a class="navbar-brand" href="#">'+
                                    '<img src="http://placehold.it/150x50&text=Logo" alt="">'+
                                '</a> -->'+
                            '</div>'+
                            '<!-- Collect the nav links, forms, and other content for toggling -->'+
                            '<div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">'+
                                '<ul class="nav navbar-nav navbar-right">'+
                            '<li><a href="/courses">Courses</a></li>'+
                            '<li><a href="/webinars">Webinars</a></li>'+
                            '<li><a href="/myaccount">My Account</a></li>'+
                            '<li><a href="/gdisconnect">Logout</a></li>'+
                          '</ul>'+
                            '</div>'+
                            '<!-- /.navbar-collapse -->'+
                        '</div>'+
                        '<!-- /.container -->'+
                    '</nav>';

var footer = '<div id="footer">'+
             'Email us : support@cocatalyst.com'+
             '</div>';

$('head').append(title);
$('body').prepend(navigationbar);
$('body').append(footer);