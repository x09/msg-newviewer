Name:          msg-newviewer
Version:       2.0
Release:       alt1
License:       %lgpl3plus
Group:         System/Configuration/Other
Source:        %name-%version.tgz
BuildArch:     noarch

Summary:       MSG NewViewer - Microsoft Outlook .msg file viewer
Url:           https://github.com/x09/msg-newviewer

BuildRequires: rpm-build-licenses
Requires: python3-modules-tkinter
Requires: altlinux-mime-defaults
Requires: shared-mime-info
Requires: python3-module-Pillow
Requires: xdg-utils

%description -l ru_RU.UTF-8
MSG NewViewer — лёгкий просмотрщик сохраненных файлов электронной почты
Microsoft Outlook (.msg), не требующий установленного Microsoft Outlook.

Реализация основана на открытых спецификациях Microsoft:
  [MS-CFB]    — Compound File Binary File Format (OLE-хранилище,
                заголовок, сектора FAT/DIFAT/MiniFAT, каталог)
  [MS-OXMSG]  — Outlook Item (.msg) File Format (потоки __substg1.0_XXXXTTTT,
                __properties_version1.0, хранилища __recip_version1.0_#N,
                __attach_version1.0_#N, вложенные письма 3701000D)
  [MS-OXPROPS] — каталог тегов и типов данных MAPI

Возможности:
  - Просмотр заголовков, тела письма, вложений и получателей
  - Поддержка вложенных сообщений и встроенных объектов
  - Доступны режимы командной строки (конвертация и извлечение) и графического интерфейса
  - Не требует проприетарных зависимостей

%description
MSG NewViewer is a lightweight viewer for Microsoft Outlook email files (.msg)
that does not require Microsoft Outlook to be installed.

The implementation is based on open Microsoft specifications:
  - [MS-CFB]    — Compound File Binary File Format (OLE storage,
                  header, FAT/DIFAT/MiniFAT sectors, directory)
  - [MS-OXMSG]  — Outlook Item (.msg) File Format (__substg1.0_XXXXTTTT streams,
                  __properties_version1.0, __recip_version1.0_#N storages,
                  __attach_version1.0_#N storages, nested messages 3701000D)
  - [MS-OXPROPS] — MAPI property tags and data types catalog

Features:
  - View message headers, body, attachments and recipients
  - Support for nested messages and embedded objects
  - Command-line and GUI modes available
  - No proprietary dependencies required

%prep
%setup

%install
mkdir -p %buildroot/%_bindir
install -m755 %name %buildroot/%_bindir/%name

mkdir -p %buildroot/%_xdgmimedir/packages/
install -m644 application-vnd.ms-outlook.xml %buildroot%_xdgmimedir/packages/application-vnd.ms-outlook.xml

mkdir -p %buildroot/%_desktopdir/
install -m644 %name.desktop %buildroot%_desktopdir/%name.desktop

#icons
mkdir -p %buildroot%_iconsdir/hicolor/scalable/apps
install -m644 icons/msg-newviewer.svg %buildroot%_iconsdir/hicolor/scalable/apps/
for s in 16 24 32 48 64 128 256 512; do
  mkdir -p %buildroot%_iconsdir/hicolor/${s}x${s}/apps
  install -m644 icons/msg-newviewer-$s.png %buildroot%_iconsdir/hicolor/${s}x${s}/apps/msg-newviewer.png
done


%post
NFILE=/etc/xdg/mimeapps.list
NMIME=application/vnd.ms-outlook
NDESKTOP=%name.desktop
touch "$NFILE"
awk -v mime="$NMIME" -v app="$NDESKTOP" '
  /^\[/ {
    if (insec && !done) { print mime "=" app; done=1 }
    insec = ($0 == "[Default Applications]")
    if (insec) hassec=1
    print; next
  }
  insec && index($0, mime "=")==1 {
    if (!done) { print mime "=" app; done=1 }
    next
  }
  { print }
  END {
    if (insec && !done) { print mime "=" app; done=1 }
    if (!hassec) { print "[Default Applications]"; print mime "=" app }
  }
' "$NFILE" > "$NFILE.tmp" && mv "$NFILE.tmp" "$NFILE"

update-mime-database %_datadir/mime ||:
update-desktop-database %_desktopdir ||:

%postun
if [ "$1" = 0 ]; then
    sed -i '/^application\/vnd\.ms-outlook=/d' /etc/xdg/mimeapps.list 2>/dev/null ||:
fi
update-mime-database %_datadir/mime ||:
update-desktop-database %_desktopdir ||:

%files
%_bindir/%name
%_iconsdir/*
%_desktopdir/%name.desktop
%_xdgmimedir/packages/application-vnd.ms-outlook.xml

%changelog
* Wed Jul 22 2026 Anton Shevtsov <shevtsov.anton@gmail.com> 2.0-alt1
- Show first 5 recipients explicitly, collapse the rest under "(N more recipients)" link
- Render inline images (jpg/png/gif) directly within the message body
- Add PIL/Pillow support for JPEG decoding and scaling of oversized images
- Double-click an attachment to open it via xdg-open (saved to a temp dir)

* Wed Jul 22 2026 Anton Shevtsov <shevtsov.anton@gmail.com> 1.0-alt1
- First version
