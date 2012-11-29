# TODO
# - bundles SWFObject v2.2 and SWFUpload
# NOTE
# - the HTML5 version, is not available as Flash version
%define		plugin	uploadify
%define		basever	3.1
Summary:	Flash Multiple File Upload jQuery Plugin Script
Name:		jquery-%{plugin}
Version:	3.1.1
Release:	0.13
License:	MIT
Group:		Applications/WWW
Source0:	http://www.uploadify.com/wp-content/uploads/files/uploadify-v%{basever}.zip
# Source0-md5:	630e0445508c9614a8d37781068073cd
Patch0:		css-path.patch
Patch1:		jquery-ns.patch
URL:		http://www.uploadify.com/
BuildRequires:	closure-compiler
BuildRequires:	js
BuildRequires:	rpmbuild(macros) >= 1.553
BuildRequires:	unzip
BuildRequires:	yuicompressor
Requires:	jquery
Requires:	js-swfobject >= 2.2
Requires:	js-swfupload >= 2.2.0.1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_datadir}/jquery/%{plugin}

%description
jQuery Multiple File Upload Plugin - Uploadify.

%prep
%setup -qc
%undos -f php,txt,css,js
%patch0 -p1
%patch1 -p1

mv "Change Log.txt" "ChangeLog.txt"

install -d examples
mv .htaccess *.php examples

# keep original for reference
cp -p jquery.uploadify-%{basever}.js{,.bak}

# unmodified swfupload 2.2
%{__sed} -i -e 1,59d jquery.uploadify-%{basever}.js

# unmmodified 2.2.0.1
%{__sed} -i -e 1,14d jquery.uploadify-%{basever}.js

%build
install -d build

# compress .js
for js in jquery.%{plugin}-%{basever}.js; do
	out=build/${js#*/}
%if 0%{!?debug:1}
	closure-compiler --js $js --charset UTF-8 --js_output_file $out
	js -C -f $out
%else
	cp -p $js $out
%endif
done

# pack .css
for css in *.css; do
	out=build/${css#*/}
%if 0%{!?debug:1}
	yuicompressor --charset UTF-8 $css -o $out
%else
	cp -p $css $out
%endif
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_examplesdir}/%{name}-%{version}}

cp -p build/jquery.%{plugin}-%{basever}.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.min.js
cp -p jquery.%{plugin}-%{basever}.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.js
ln -s %{plugin}-%{version}.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}.src.js
ln -s %{plugin}-%{version}.min.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}.js

cp -p %{plugin}.css $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.css
cp -p build/%{plugin}.css $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.min.css
ln -s %{plugin}-%{version}.css $RPM_BUILD_ROOT%{_appdir}/%{plugin}.src.css
ln -s %{plugin}-%{version}.min.css $RPM_BUILD_ROOT%{_appdir}/%{plugin}.css

cp -p *.png *.swf $RPM_BUILD_ROOT%{_appdir}

cp -a examples/{.*,*} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc license.txt ChangeLog.txt
%{_appdir}
%{_examplesdir}/%{name}-%{version}
