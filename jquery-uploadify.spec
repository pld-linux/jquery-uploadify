# TODO
# - includes bundled SWFObject v2.2 and SWFUpload
# - fix img path in .css file, pack css
# NOTE
# - the HTML5 version, is not available as Flash version
%define		plugin	uploadify
%define		basever	3.1
Summary:	Flash Multiple File Upload jQuery Plugin Script
Name:		jquery-%{plugin}
Version:	3.1.1
Release:	0.2
License:	MIT
Group:		Applications/WWW
Source0:	http://www.uploadify.com/wp-content/uploads/files/uploadify-v%{basever}.zip
# Source0-md5:	630e0445508c9614a8d37781068073cd
URL:		http://www.uploadify.com/
BuildRequires:	rpmbuild(macros) >= 1.553
BuildRequires:	unzip
Requires:	jquery >= 1.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_datadir}/jquery/%{plugin}

%description
jQuery Multiple File Upload Plugin - Uploadify.

%prep
%setup -qc

mv "Change Log.txt" "ChangeLog.txt"

%undos -f php,txt

install -d examples
mv .htaccess *.php examples

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_examplesdir}/%{name}-%{version}}

cp -p jquery.%{plugin}-%{basever}.min.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.min.js
cp -p jquery.%{plugin}-%{basever}.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.js
ln -s %{plugin}-%{version}.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}.src.js
ln -s %{plugin}-%{version}.min.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}.js
cp -p *.png *.swf $RPM_BUILD_ROOT%{_appdir}
cp -p *.css $RPM_BUILD_ROOT%{_appdir}

cp -a examples/{.*,*} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc license.txt ChangeLog.txt
%{_appdir}
%{_examplesdir}/%{name}-%{version}
