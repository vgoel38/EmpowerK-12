var title = '<title>CoCatalyst</title>';
var styles = '<style>'+
                '.navLink:hover{'+
                    'background-color:#52504E'+
                '}'+
                '.dropdown{'+
                    'position: relative;'+
                    'display: inline-block;'+
                '}'+
                '.dropdown-content {'+
                    'display: none;'+
                    'position: absolute;'+
                    'background-color: #222222;'+
                    'min-width: 250px;'+
                    'box-shadow:0px 8px 16px 0px rgba(0,0,0,0.2);'+
                    'padding: 12px 16px;'+
                    'z-index: 1;'+
                '}'+
                '.dropdown:hover .dropdown-content{'+
                    'display: block;'+
                '}'+
             '</style>';
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
                                    '<li class="navLink dropdown">'+
                                        '<a href="/courses">Courses</a>'+
                                            '<div class="dropdown-content">'+
                                                '<ul class="nav navbar-nav">'+
                                                '<li class="navLink"><a href="/memory">Photographic Memory Course</a></li>'+
                                                '<li class="navLink"><a href="/android">Android Apps and Games Development</a></li>'+
                                                '</ul>'+
                                            '</div>'+
                                    '</li>'+
                                    '<li class="navLink"><a href="/webinars">Webinars</a></li>'+
                                    '<li class="navLink"><a href="/faqs">FAQs</a></li>'+
                                    '<li class="navLink"><a href="/logout">Logout</a></li>'+
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
$('head').append(styles);
$('body').prepend(navigationbar);
$('body').append(footer);