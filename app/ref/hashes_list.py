HASHS_LIST = [
	{
		"code": "14100",
		"name": "3DES (PT = $salt, key = $pass)",
		"example": "37387ff8d8dafe15:8152001061460743",
	},
	{
		"code": "11600",
		"name": "7-Zip",
		"example": "$7z$0$19$0$salt$8$f6196259a7326e3f0000000000000000$185065650$112$98$f3bc2a88062c419a25acd40c0c2d75421cf23263f69c51b13f9b1aada41a8a09f9adeae45d67c60b56aad338f20c0dcc5eb811c7a61128ee0746f922cdb9c59096869f341c7a9cb1ac7bb7d771f546b82cf4e6f11a5ecd4b61751e4d8de66dd6e2dfb5b7d1022d2211e2d66ea1703f96",
	},
	{
		"code": "6300",
		"name": "AIX {smd5}",
		"example": "{smd5}a5/yTL/u$VfvgyHx1xUlXZYBocQpQY0",
	},
	{
		"code": "6700",
		"name": "AIX {ssha1}",
		"example": "{ssha1}06$bJbkFGJAB30L2e23$dCESGOsP7jaIIAJ1QAcmaGeG.kr",
	},
	{
		"code": "6400",
		"name": "AIX {ssha256}",
		"example": "{ssha256}06$aJckFGJAB30LTe10$ohUsB7LBPlgclE3hJg9x042DLJvQyxVCX.nZZLEz.g2",
	},
	{
		"code": "6500",
		"name": "AIX {ssha512}",
		"example": "{ssha512}06$bJbkFGJAB30L2e23$bXiXjyH5YGIyoWWmEVwq67nCU5t7GLy9HkCzrodRCQCx3r9VvG98o7O3V0r9cVrX3LPPGuHqT5LLn0oGCuI1..",
	},
	{
		"code": "12900",
		"name": "Android FDE (Samsung DEK)",
		"example": "38421854118412625768408160477112384218541184126257684081604771129b6258eb22fc8b9d08e04e6450f72b98725d7d4fcad6fb6aec4ac2a79d0c6ff738421854118412625768408160477112",
	},
	{
		"code": "125",
		"name": "ArubaOS",
		"example": "5387280701327dc2162bdeb451d5a465af6d13eff9276efeba",
	},
	{
		"code": "13200",
		"name": "AxCrypt",
		"example": "$axcrypt$*1*10000*aaf4a5b4a7185551fea2585ed69fe246*45c616e901e48c6cac7ff14e8cd99113393be259c595325e",
	},
	{
		"code": "13300",
		"name": "AxCrypt in memory SHA1",
		"example": "$axcrypt_sha1$b89eaac7e61417341b710b727768294d0e6a277b",
	},
	{
		"code": "1431",
		"name": "base64(sha256(unicode($pass)))",
		"example": "npKD5jP0p6QtOryTcBFVvor+VmDaJMh1jn01M+Ly3II=",
	},
	{
		"code": "3200",
		"name": "bcrypt, Blowfish(OpenBSD)",
		"example": "$2a$05$LhayLxezLhK1LhWvKxCyLOj0j1u.Kj0jZ0pEmm134uzrQlFvQJLF6",
	},
	{
		"code": "11300",
		"name": "Bitcoin/Litecoin wallet.dat",
		"example": "$bitcoin$96$d011a1b6a8d675b7a36d0cd2efaca32a9f8dc1d57d6d01a58399ea04e703e8bbb44899039326f7a00f171a7bbc854a54$16$1563277210780230$158555$96$628835426818227243334570448571536352510740823233055715845322741625407685873076027233865346542174$66$625882875480513751851333441623702852811440775888122046360561760525",
	},
	{
		"code": "12700",
		"name": "Blockchain, My Wallet",
		"example": "$blockchain$288$5420055827231730710301348670802335e45a6f5f631113cb1148a6e96ce645ac69881625a115fd35256636d0908217182f89bdd53256a764e3552d3bfe68624f4f89bb6de60687ff1ebb3cbf4e253ee3bea0fe9d12d6e8325ddc48cc924666dc017024101b7dfb96f1f45cfcf642c45c83228fe656b2f88897ced2984860bf322c6a89616f6ea5800aadc4b293ddd46940b3171a40e0cca86f66f0d4a487aa3a1beb82569740d3bc90bc1cb6b4a11bc6f0e058432cc193cb6f41e60959d03a84e90f38e54ba106fb7e2bfe58ce39e0397231f7c53a4ed4fd8d2e886de75d2475cc8fdc30bf07843ed6e3513e218e0bb75c04649f053a115267098251fd0079272ec023162505725cc681d8be12507c2d3e1c9520674c68428df1739944b8ac",
	},
	{
		"code": "12400",
		"name": "BSDiCrypt, Extended DES",
		"example": "_9G..8147mpcfKT8g0U.",
	},
	{
		"code": "2410",
		"name": "Cisco-ASA MD5",
		"example": "02dMBMYkTdC5Ziyp:36",
	},
	{
		"code": "5700",
		"name": "Cisco-IOS SHA256",
		"example": "2btjjy78REtmYkkW0csHUbJZOstRXoWdX1mGrmmfeHI",
	},
	{
		"code": "2400",
		"name": "Cisco-PIX MD5",
		"example": "dRRVnUmUHXOTt9nk",
	},
	{
		"code": "8100",
		"name": "Citrix Netscaler",
		"example": "1765058016a22f1b4e076dccd1c3df4e8e5c0839ccded98ea",
	},
	{
		"code": "12600",
		"name": "ColdFusion 10+",
		"example": "aee9edab5653f509c4c63e559a5e967b4c112273bc6bd84525e630a3f9028dcb:5136256866783777334574783782810410706883233321141647265340462733",
	},
	{
		"code": "10200",
		"name": "Cram MD5",
		"example": "$cram_md5$PG5vLXJlcGx5QGhhc2hjYXQubmV0Pg==$dXNlciA0NGVhZmQyMmZlNzY2NzBmNmIyODc5MDgxYTdmNWY3MQ==",
	},
	{
		"code": "11500",
		"name": "CRC32",
		"example": "c762de4a:00000000",
	},
	{
		"code": "14000",
		"name": "DES (PT = $salt, key = $pass)",
		"example": "a28bc61d44bb815c:1172075784504605",
	},
	{
		"code": "1500",
		"name": "descrypt, DES(Unix), Traditional DES",
		"example": "48c/R8JAv757A",
	},
	{
		"code": "10000",
		"name": "Django (PBKDF2-SHA256)",
		"example": "pbkdf2_sha256$20000$H0dPx8NeajVu$GiC4k5kqbbR9qWBlsRgDywNqC2vd9kqfk7zdorEnNas=",
	},
	{
		"code": "124",
		"name": "Django (SHA-1)",
		"example": "sha1$fe76b$02d5916550edf7fc8c886f044887f4b1abf9b013",
	},
	{
		"code": "8300",
		"name": "DNSSEC (NSEC3)",
		"example": "7b5n74kq8r441blc2c5qbbat19baj79r:.lvdsiqfj.net:33164473:1",
	},
	{
		"code": "1100",
		"name": "Domain Cached Credentials (DCC), MS Cache",
		"example": "4dd8965d1d476fa0d026722989a6b772:3060147285011",
	},
	{
		"code": "7900",
		"name": "Drupal7",
		"example": "$S$C33783772bRXEx1aCsvY.dqgaaSu76XmVlKrW9Qu8IQlvxHlmzLf",
	},
	{
		"code": "12200",
		"name": "eCryptfs",
		"example": "$ecryptfs$0$1$7c95c46e82f364b3$60bba503f0a42d0c",
	},
	{
		"code": "123",
		"name": "EPi",
		"example": "0x326C6D7B4E4F794B79474E36704F35723958397163735263516265456E31 0xAFC55E260B8F45C0C6512BCE776C1AD8312B56E6",
	},
	{
		"code": "141",
		"name": "EPiServer 6.x < v4",
		"example": "$episerver$*0*bEtiVGhPNlZpcUN4a3ExTg==*utkfN0EOgljbv5FoZ6+AcZD5iLk",
	},
	{
		"code": "1441",
		"name": "EPiServer 6.x >= v4",
		"example": "$episerver$*1*MDEyMzQ1Njc4OWFiY2RlZg==*lRjiU46qHA7S6ZE7RfKUcYhB85ofArj1j7TrCtu3u6Y",
	},
	{
		"code": "7000",
		"name": "Fortigate (FortiOS)",
		"example": "AK1AAECAwQFBgcICRARNGqgeC3is8gv2xWWRony9NJnDgEA",
	},
	{
		"code": "11700",
		"name": "GOST R 34.11-2012 (Streebog) 256-bit",
		"example": "57e9e50caec93d72e9498c211d6dc4f4d328248b48ecf46ba7abfa874f666e36",
	},
	{
		"code": "11800",
		"name": "GOST R 34.11-2012 (Streebog) 512-bit",
		"example": "5d5bdba48c8f89ee6c0a0e11023540424283e84902de08013aeeb626e819950bb32842903593a1d2e8f71897ff7fe72e17ac9ba8ce1d1d2f7e9c4359ea63bdc3",
	},
	{
		"code": "6900",
		"name": "GOST R 34.11-94",
		"example": "df226c2c6dcb1d995c0299a33a084b201544293c31fc3d279530121d36bbcea9",
	},
	{
		"code": "7200",
		"name": "GRUB 2",
		"example": "grub.pbkdf2.sha512.10000.7d391ef48645f626b427b1fae06a7219b5b54f4f02b2621f86b5e36e83ae492bd1db60871e45bc07925cecb46ff8ba3db31c723c0c6acbd4f06f60c5b246ecbf.26d59c52b50df90d043f070bd9cbcd92a74424da42b3666fdeb08f1a54b8f1d2f4f56cf436f9382419c26798dc2c209a86003982b1e5a9fcef905f4dfaa4c524",
	},
	{
		"code": "5100",
		"name": "Half MD5",
		"example": "8743b52063cd8409",
	},
	{
		"code": "50",
		"name": "HMAC-MD5 (key = $pass)",
		"example": "fc741db0a2968c39d9c2a5cc75b05370:1234",
	},
	{
		"code": "60",
		"name": "HMAC-MD5 (key = $salt)",
		"example": "bfd280436f45fa38eaacac3b00518f29:1234",
	},
	{
		"code": "150",
		"name": "HMAC-SHA1 (key = $pass)",
		"example": "c898896f3f70f61bc3fb19bef222aa860e5ea717:1234",
	},
	{
		"code": "160",
		"name": "HMAC-SHA1 (key = $salt)",
		"example": "d89c92b4400b15c39e462a8caa939ab40c3aeeea:1234",
	},
	{
		"code": "1450",
		"name": "HMAC-SHA256 (key = $pass)",
		"example": "abaf88d66bf2334a4a8b207cc61a96fb46c3e38e882e6f6f886742f688b8588c:1234",
	},
	{
		"code": "1460",
		"name": "HMAC-SHA256 (key = $salt)",
		"example": "8efbef4cec28f228fa948daaf4893ac3638fbae81358ff9020be1d7a9a509fc6:1234",
	},
	{
		"code": "1750",
		"name": "HMAC-SHA512 (key = $pass)",
		"example": "94cb9e31137913665dbea7b058e10be5f050cc356062a2c9679ed0ad6119648e7be620e9d4e1199220cd02b9efb2b1c78234fa1000c728f82bf9f14ed82c1976:1234",
	},
	{
		"code": "1760",
		"name": "HMAC-SHA512 (key = $salt)",
		"example": "7cce966f5503e292a51381f238d071971ad5442488f340f98e379b3aeae2f33778e3e732fcc2f7bdc04f3d460eebf6f8cb77da32df25500c09160dd3bf7d2a6b:1234",
	},
	{
		"code": "1421",
		"name": "hMailServer",
		"example": "8fe7ca27a17adc337cd892b1d959b4e487b8f0ef09e32214f44fb1b07e461c532e9ec3",
	},
	{
		"code": "2811",
		"name": "IPB2+, MyBB1.2+",
		"example": "8d2129083ef35f4b365d5d87487e1207:47204",
	},
	{
		"code": "7300",
		"name": "IPMI2 RAKP HMAC-SHA1",
		"example": "b7c2d6f13a43dce2e44ad120a9cd8a13d0ca23f0414275c0bbe1070d2d1299b1c04da0f1a0f1e4e2537300263a2200000000000000000000140768617368636174:472bdabe2d5d4bffd6add7b3ba79a291d104a9ef",
	},
	{
		"code": "14700",
		"name": "iTunes Backup < 10.0",
		"example": "$itunes_backup$*9*b8e3f3a970239b22ac199b622293fe4237b9d16e74bad2c3c3568cd1bd3c471615a6c4f867265642*10000*4542263740587424862267232255853830404566**",
	},
	{
		"code": "14800",
		"name": "iTunes Backup >= 10.0",
		"example": "$itunes_backup$*10*8b715f516ff8e64442c478c2d9abb046fc6979ab079007d3dbcef3ddd84217f4c3db01362d88fa68*10000*2353363784073608264337337723324886300850*10000000*425b4bb4e200b5fd4c66979c9caca31716052063",
	},
	{
		"code": "11",
		"name": "Joomla < 2.5.18",
		"example": "19e0e8d91c722e7091ca7a6a6fb0f4fa:54718031842521651757785603028777",
	},
	{
		"code": "22",
		"name": "Juniper Netscreen/SSG (ScreenOS)",
		"example": "nNxKL2rOEkbBc9BFLsVGG6OtOUO/8n:user",
	},
	{
		"code": "13400",
		"name": "Keepass 1 AES / without keyfile",
		"example": "$keepass$*1*50000*0*375756b9e6c72891a8e5645a3338b8c8*82afc053e8e1a6cfa39adae4f5fe5e59f545a54d6956593d1709b39cacd7f796*c698fbfc7d1b71431d10611e2216ab21*24a63140f4eb3bfd7d59b7694eea38d1d93a43bc3af989755d2b326286c4d510*1*192*1a65072f436e9da0c9e832eca225a04ab78821b55d9f550860ade2ef8126a2c4050cf4d033374abd3dac6d0c5907c6cbb033643b203825c12e6c9853b5ac17a4809559fe723e01b4a2ab87cc83c8ba7ee4a757b8a0cf1674106f21f6675cba12064443d65436650df10ea0923c4cadfd4bfe341a6f4fa23a1a67f7d12a489fc5410ef6db9f6607905de491d3b3b915852a1b6c231c96366cbdee5ea9bd7f73ffd2f7a579215528ae1bf0ea540947ebfe39ca84bc6cbeded4f8e8fb6ed8f32dd5",
	},
	{
		"code": "13400",
		"name": "Keepass 1 Twofish / with keyfile",
		"example": "$keepass$*1*6000*1*31c087828b0bb76362c10cae773aacdf*6d6c78b4f82ecbcd3b96670cf490914c25ea8c31bc3aeb3fc56e65fac16d721f*a735ec88c01816bc66200c8e17ee9110*08334be8523f4b69bd4e2328db854329bfc81e2ea5a46d8ccf3bccf7c03d879d*1*1360*f1e2c6c47f88c2abf4e79dbe73339b77778233a6c7d7f49f6b7d5db6a4885ff33585e221f5e94e8f7cc84ddcbe9c61a3d40c4f503a4ec7e91edca5745454588eebb4f0dc4d251c0d88eb5fae5d5b651d16e56ef830f412cb7fccf643de4963b66852d3a775489b5abb394b6fa325c3dbb4a55dd06d44c5fc911f1305e55accf0dc0eb172788f5400aab3c867cc6c5ddb7cd3e57bb78a739416985a276825171f5a19750dede055aa3e5fca9b11e3606beae97d68e593631a2efd88cdeb9f43b5ac1d1d9f0164f0fb022ea44a4a48061629c83d8f5bc594e3655ee684102fe706d1e96178bb805105fe1c5326c951401a6e7c9a0b8b572e7b74c3fb25e8700a2e0e70b4621ae3878805397ea1b873ea5218fdaa4fc5d11cdf7ea3579601eca3750fa347edc08569b1f51606d35920253f85f33e6a757a585adf079173161af919f7ea0d78ca6ca1513d01855057373c4f9fe22aba1fc4b18708d329500c127b865a528435e9e00d0a80554ae6eaf4d58bf85a959f37d0854b36c782991c36120b41ee2d9905b18d525b6bffef310e90dbfbe9be853614e6559737f1141f725902f59ee02789c6490c16adf0957e36dc4101c57ba35acb4ca9ec60f5585b60e74342921bbc7e56df5ad942b6deb7936532439b1dae39b9709cf282239c57b434d6f65ba277012ccddce32a217964f974c16f96d8b078ceaad43de9f3d5309279843f2f347ad8ae6eab3a998bb99a421b22b806e2f2302f9dcf3ba54e3d3f1ee64ef3b202194912eec202c2f44847ad5293b03b6b22df35f505670a79219efc399c6a4fa3fd4be7953e5df9baf94101c0a7036b82b6950ab2b722e38aec47bf1c7ffb4e82f43b9ca18d2a8b0b2a7b92015b01d07a429d2660902185cf143f871ff49dde73acf7c3bfd9c124733bd90ffe0fd1cc9090d56dd70bd62f9df1bfa4748ea3438f669d5691c61ec7fbc9d53ab4d8c2dda2cf203f7a5a7fac72eb2efe1d9a27b8c5b14e07a55c530dfd7b7c69dcf478590b7b364f5379f92a0762be0005c4cbc5285d7828248159286fe6d29c02c7de04e96e737a2d30ce75ff774982433f75ca16f09ad668e5b13f0a2e84886773d8fff67f71c1a9dab13f78e5b2da9b1eed9ab2208934a6da7eab32b3e8da1599d6cfa7e9c19ad8efc85dd9a2a4b95832c435381c2fe7e44c58045ce91e40d58c36924b38b19cbafd696bac8761229de9099ce31ee1c93a98aa0cb2a7c60b71b7f1998690e5eae623827727cfe7e8eed94ffc927a1e15aac32292daccda4f0d35383ce87f7e872fc3fe8f01f4a44de4f7b76257abc9c056ab8ae0d96d2dc3a154408c28a2e7befbd515cb5013cbfed31af456ac2b596b5d8095420c411b981d48741dc7ed1e8de4e428bd5e5a553348e2890b1ed12b7dc88261ab921a12da43e6344bbb4a0e0ce2b84c2d1d6c1f51b88202743433ac24340ae00cf27d43346240f4dc5e35ec29fcf1bf6de3bcc09ee8db3f49c3b6615bd8796bbe2cf4b914766779408e772123d9e51cc92ed5dedafa427fd767198cb97674eded4e4df84716aec75cbe7a54620c283fa60780be3cd66ea4167f46cdea1506be92a5102317c8ab8be097c993d82bd831818fe7cb1fbfecc3432d93e0f6d36da8a65ed15c78e623d59980be7ff54bdb1786de2ca9e7a11f0fe067db9ec42ade3bbaad10adae5ea77ba76fa2d0723a35891bde91da540a58e343c23afa9e22b38a66171eb9dbbd55f9e0f014e9de3943388fe0990cc801bbb978c02bf680b3c63a747e22a6317440c40e6844987e936c88c25f49e601ec3486ab080165b5e01dbee47a0a385dfba22ec5ed075f94052bdddabde761bbcc79852402c5b22ded89af4c602922099e37d71b7f87f4ffa614b4ca106fca6b062cba350be1fd12c6812db82f3e02a81e42*1*64*bbc3babf62557aa4dfba705e24274e1aebf43907fe12f52eaf5395066f7cbdba",
	},
	{
		"code": "13400",
		"name": "Keepass 2 AES / with keyfile",
		"example": "$keepass$*2*6000*222*15b6b685bae998f2f608c909dc554e514f2843fbac3c7c16ea3600cc0de30212*c417098b445cfc7a87d56ba17200836f30208d38f75a4169c0280bab3b10ca2a*0d15a81eadccc58b1d3942090cd0ba66*57c4aa5ac7295a97da10f8b2f2d2bfd7a98b0faf75396bc1b55164a1e1dc7e52*2b822bb7e7d060bb42324459cb24df4d3ecd66dc5fc627ac50bf2d7c4255e4f8*1*64*aaf72933951a03351e032b382232bcafbeeabc9bc8e6988b18407bc5b8f0e3cc",
	},
	{
		"code": "13400",
		"name": "Keepass 2 AES / without keyfile",
		"example": "$keepass$*2*6000*222*a279e37c38b0124559a83fa452a0269d56dc4119a5866d18e76f1f3fd536d64d*7ec7a06bc975ea2ae7c8dcb99e826a308564849b6b25d858cbbc78475af3733f*d477c849bf2278b7a1f626c81e343553*38c8ec186141c2705f2bcb334a730933ed3b0ee11391e1100fbaf429f6c99078*1ada85fe78cf36ab0537562a787dd83e446f13cd3d9a60fd495003de3537b702",
	},
	{
		"code": "7500",
		"name": "Kerberos 5 AS-REQ Pre-Auth",
		"example": "$krb5pa$23$user$realm$salt$4e751db65422b2117f7eac7b721932dc8aa0d9966785ecd958f971f622bf5c42dc0c70b532363138363631363132333238383835",
	},
	{
		"code": "13100",
		"name": "Kerberos 5 TGS-REP etype 23",
		"example": "$krb5tgs$23$*user$realm$test/spn*$63386d22d359fe42230300d56852c9eb$891ad31d09ab89c6b3b8c5e5de6c06a7f49fd559d7a9a3c32576c8fedf705376cea582ab5938f7fc8bc741acf05c5990741b36ef4311fe3562a41b70a4ec6ecba849905f2385bb3799d92499909658c7287c49160276bca0006c350b0db4fd387adc27c01e9e9ad0c20ed53a7e6356dee2452e35eca2a6a1d1432796fc5c19d068978df74d3d0baf35c77de12456bf1144b6a750d11f55805f5a16ece2975246e2d026dce997fba34ac8757312e9e4e6272de35e20d52fb668c5ed",
	},
	{
		"code": "6800",
		"name": "Lastpass",
		"example": "a2d1f7b7a1862d0d4a52644e72d59df5:500:lp@trash-mail.com",
	},
	{
		"code": "3000",
		"name": "LM",
		"example": "299bd128c1101fd6",
	},
	{
		"code": "8600",
		"name": "Lotus Notes/Domino 5",
		"example": "3dd2e1e5ac03e230243d58b8c5ada076",
	},
	{
		"code": "8700",
		"name": "Lotus Notes/Domino 6",
		"example": "(GDpOtD35gGlyDksQRxEU)",
	},
	{
		"code": "9100",
		"name": "Lotus Notes/Domino 8",
		"example": "(HsjFebq0Kh9kH7aAZYc7kY30mC30mC3KmC30mCluagXrvWKj1)",
	},
	{
		"code": "900",
		"name": "MD4",
		"example": "afe04867ec7a3845145579a95f72eca7",
	},
	{
		"code": "0",
		"name": "MD5",
		"example": "8743b52063cd84097a65d1633f5c74f5",
	},
	{
		"code": "10",
		"name": "md5($pass.$salt)",
		"example": "01dfae6e5d4d90d9892622325959afbe:7050461",
	},
	{
		"code": "3720",
		"name": "md5($pass.md5($salt))",
		"example": "10ce488714fdbde9453670e0e4cbe99c:1234",
	},
	{
		"code": "20",
		"name": "md5($salt.$pass)",
		"example": "f0fda58630310a6dd91a7d8f0a4ceda2:4225637426",
	},
	{
		"code": "3800",
		"name": "md5($salt.$pass.$salt)",
		"example": "2e45c4b99396c6cb2db8bda0d3df669f:1234",
	},
	{
		"code": "3710",
		"name": "md5($salt.md5($pass))",
		"example": "95248989ec91f6d0439dbde2bd0140be:1234",
	},
	{
		"code": "4110",
		"name": "md5($salt.md5($pass.$salt))",
		"example": "b4cb5c551a30f6c25d648560408df68a:1234",
	},
	{
		"code": "4010",
		"name": "md5($salt.md5($salt.$pass))",
		"example": "30d0cf4a5d7ed831084c5b8b0ba75b46:1234",
	},
	{
		"code": "40",
		"name": "md5($salt.unicode($pass))",
		"example": "d63d0e21fdc05f618d55ef306c54af82:13288442151473",
	},
	{
		"code": "4210",
		"name": "md5($username.0.$pass)",
		"example": "09ea048c345ad336ebe38ae5b6c4de24:1234",
	},
	{
		"code": "4800",
		"name": "MD5(Chap), iSCSI CHAP authentication",
		"example": "afd09efdd6f8ca9f18ec77c5869788c3:01020304050607080910111213141516:01",
	},
	{
		"code": "2600",
		"name": "md5(md5($pass))",
		"example": "a936af92b0ae20b1ff6c3347a72e5fbe",
	},
	{
		"code": "3910",
		"name": "md5(md5($pass).md5($salt))",
		"example": "250920b3a5e31318806a032a4674df7e:1234",
	},
	{
		"code": "3610",
		"name": "md5(md5($salt).$pass)",
		"example": "7b57255a15958ef898543ea6cc3313bc:1234",
	},
	{
		"code": "3500",
		"name": "md5(md5(md5($pass)))",
		"example": "9882d0778518b095917eb589f6998441",
	},
	{
		"code": "4400",
		"name": "md5(sha1($pass))",
		"example": "288496df99b33f8f75a7ce4837d1b480",
	},
	{
		"code": "4300",
		"name": "md5(strtoupper(md5($pass)))",
		"example": "b8c385461bb9f9d733d3af832cf60b27",
	},
	{
		"code": "3300",
		"name": "MD5(Sun)",
		"example": "$md5$rounds=904$iPPKEBnEkp3JV8uX$0L6m7rOFTVFn.SGqo2M9W1",
	},
	{
		"code": "30",
		"name": "md5(unicode($pass).$salt)",
		"example": "b31d032cfdcf47a399990a71e43c5d2a:144816",
	},
	{
		"code": "1600",
		"name": "md5apr1, MD5(APR), Apache MD5",
		"example": "$apr1$71850310$gh9m4xcAn3MGxogwX/ztb.",
	},
	{
		"code": "500",
		"name": "md5crypt, MD5(Unix), FreeBSD MD5, Cisco-IOS MD5",
		"example": "$1$28772684$iEwNOgGugqO9.bIz5sk8k/",
	},
	{
		"code": "3711",
		"name": "Mediawiki B type",
		"example": "$B$56668501$0ce106caa70af57fd525aeaf80ef2898",
	},
	{
		"code": "9700",
		"name": "MS Office \u21d0 2003 MD5 + RC4, oldoffice$0, oldoffice$1",
		"example": "$oldoffice$1*04477077758555626246182730342136*b1b72ff351e41a7c68f6b45c4e938bd6*0d95331895e99f73ef8b6fbc4a78ac1a",
	},
	{
		"code": "9800",
		"name": "MS Office \u21d0 2003 SHA1 + RC4, oldoffice$3, oldoffice$4",
		"example": "$oldoffice$3*83328705222323020515404251156288*2855956a165ff6511bc7f4cd77b9e101*941861655e73a09c40f7b1e9dfd0c256ed285acd",
	},
	{
		"code": "12800",
		"name": "MS-AzureSync PBKDF2-HMAC-SHA256",
		"example": "v1;PPH1_MD4,84840328224366186645,100,005a491d8bf3715085d69f934eef7fb19a15ffc233b5382d9827910bc32f3506",
	},
	{
		"code": "131",
		"name": "MSSQL(2000)",
		"example": "0x01002702560500000000000000000000000000000000000000008db43dd9b1972a636ad0c7d4b8c515cb8ce46578",
	},
	{
		"code": "132",
		"name": "MSSQL(2005)",
		"example": "0x010018102152f8f28c8499d8ef263c53f8be369d799f931b2fbe",
	},
	{
		"code": "1731",
		"name": "MSSQL(2012), MSSQL(2014)",
		"example": "0x02000102030434ea1b17802fd95ea6316bd61d2c94622ca3812793e8fb1672487b5c904a45a31b2ab4a78890d563d2fcf5663e46fe797d71550494be50cf4915d3f4d55ec375",
	},
	{
		"code": "11200",
		"name": "MySQL Challenge-Response Authentication (SHA1)",
		"example": "$mysqlna$1c24ab8d0ee94d70ab1f2e814d8f0948a14d10b9*437e93572f18ae44d9e779160c2505271f85821d",
	},
	{
		"code": "200",
		"name": "MySQL323",
		"example": "7196759210defdc0",
	},
	{
		"code": "300",
		"name": "MySQL4.1/MySQL5+",
		"example": "FCF7C1B8749CF99D88E5F34271D636178FB5D130",
	},
	{
		"code": "5500",
		"name": "NetNTLMv1-VANILLA / NetNTLMv1+ESS",
		"example": "u4-netntlm::kNS:338d08f8e26de93300000000000000000000000000000000:9526fb8c23a90751cdd619b6cea564742e1e4bf33006ba41:cb8086049ec4736c",
	},
	{
		"code": "5600",
		"name": "NetNTLMv2",
		"example": "admin::N46iSNekpT:08ca45b7d7ea58ee:88dcbe4446168966a153a0064958dac6:5c7830315c7830310000000000000b45c67103d07d7b95acd12ffa11230e0000000052920b85f78d013c31cdb3b92f5d765c783030",
	},
	{
		"code": "101",
		"name": "nsldap, SHA-1(Base64), Netscape LDAP SHA",
		"example": "{SHA}uJ6qx+YUFzQbcQtyd2gpTQ5qJ3s=",
	},
	{
		"code": "111",
		"name": "nsldaps, SSHA-1(Base64), Netscape LDAP SSHA",
		"example": "{SSHA}AZKja92fbuuB9SpRlHqaoXxbTc43Mzc2MDM1Ng==",
	},
	{
		"code": "1000",
		"name": "NTLM",
		"example": "b4b9b02e6f09a9bd760f388b67351e2b",
	},
	{
		"code": "9400",
		"name": "Office 2007",
		"example": "$office$*2007*20*128*16*411a51284e0d0200b131a8949aaaa5cc*117d532441c63968bee7647d9b7df7d6*df1d601ccf905b375575108f42ef838fb88e1cde",
	},
	{
		"code": "13900",
		"name": "OpenCart",
		"example": "6e36dcfc6151272c797165fce21e68e7c7737e40:472433673",
	},
	{
		"code": "3100",
		"name": "Oracle H: Type (Oracle 7+), DES(Oracle)",
		"example": "7A963A529D2E3229:3682427524",
	},
	{
		"code": "112",
		"name": "Oracle S: Type (Oracle 11+)",
		"example": "ac5f1e62d21fd0529428b84d42e8955b04966703:38445748184477378130",
	},
	{
		"code": "12300",
		"name": "Oracle T: Type (Oracle 12+)",
		"example": "78281A9C0CF626BD05EFC4F41B515B61D6C4D95A250CD4A605CA0EF97168D670EBCB5673B6F5A2FB9CC4E0C0101E659C0C4E3B9B3BEDA846CD15508E88685A2334141655046766111066420254008225",
	},
	{
		"code": "21",
		"name": "osCommerce, xt:Commerce",
		"example": "374996a5e8a5e57fd97d893f7df79824:36",
	},
	{
		"code": "11900",
		"name": "PBKDF2-HMAC-MD5",
		"example": "md5:1000:MTg1MzA=:Lz84VOcrXd699Edsj34PP98+f4f3S0rTZ4kHAIHoAjs=",
	},
	{
		"code": "12000",
		"name": "PBKDF2-HMAC-SHA1",
		"example": "sha1:1000:MzU4NTA4MzIzNzA1MDQ=:19ofiY+ahBXhvkDsp0j2ww==",
	},
	{
		"code": "10900",
		"name": "PBKDF2-HMAC-SHA256",
		"example": "sha256:1000:MTc3MTA0MTQwMjQxNzY=:PYjCU215Mi57AYPKva9j7mvF4Rc5bCnt",
	},
	{
		"code": "12100",
		"name": "PBKDF2-HMAC-SHA512",
		"example": "sha512:1000:ODQyMDEwNjQyODY=:MKaHNWXUsuJB3IEwBHbm3w==",
	},
	{
		"code": "10400",
		"name": "PDF 1.1 - 1.3 (Acrobat 2 - 4)",
		"example": "$pdf$1*2*40*-1*0*16*51726437280452826511473255744374*32*9b09be05c226214fa1178342673d86f273602b95104f2384b6c9b709b2cbc058*32*0000000000000000000000000000000000000000000000000000000000000000",
	},
	{
		"code": "10500",
		"name": "PDF 1.4 - 1.6 (Acrobat 5 - 8)",
		"example": "$pdf$2*3*128*-1028*1*16*da42ee15d4b3e08fe5b9ecea0e02ad0f*32*c9b59d72c7c670c42eeb4fca1d2ca15000000000000000000000000000000000*32*c4ff3e868dc87604626c2b8c259297a14d58c6309c70b00afdfb1fbba10ee571",
	},
	{
		"code": "10600",
		"name": "PDF 1.7 Level 3 (Acrobat 9)",
		"example": "$pdf$5*5*256*-1028*1*16*20583814402184226866485332754315*127*f95d927a94829db8e2fbfbc9726ebe0a391b22a084ccc2882eb107a74f7884812058381440218422686648533275431500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000*127*00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000*32*0000000000000000000000000000000000000000000000000000000000000000*32*0000000000000000000000000000000000000000000000000000000000000000",
	},
	{
		"code": "10700",
		"name": "PDF 1.7 Level 8 (Acrobat 10 - 11)",
		"example": "$pdf$5*6*256*-4*1*16*381692e488413f5502fa7314a78c25db*48*e5bf81a2a23c88f3dccb44bc7da68bb5606b653b733bcf9adaa5eb2c8ccf53abba66539044eb1957eda68469b1d0b9b5*48*b222df06deb308bf919d13447e688775fdcab972faed2c866dc023a126cb4cd4bbffab3683ecde243cf8d88967184680",
	},
	{
		"code": "133",
		"name": "PeopleSoft",
		"example": "uXmFVrdBvv293L9kDR3VnRmx4ZM=",
	},
	{
		"code": "13500",
		"name": "PeopleSoft PS_TOKEN",
		"example": "b5e335754127b25ba6f99a94c738e24cd634c35a:aa07d396f5038a6cbeded88d78d1d6c907e4079b3dc2e12fddee409a51cc05ae73e8cc24d518c923a2f79e49376594503e6238b806bfe33fa8516f4903a9b4",
	},
	{
		"code": "400",
		"name": "phpass, MD5(phpBB3)",
		"example": "$H$984478476IagS59wHZvyQMArzfx58u.",
	},
	{
		"code": "400",
		"name": "phpass, MD5(Wordpress),",
		"example": "$P$984478476IagS59wHZvyQMArzfx58u.",
	},
	{
		"code": "2612",
		"name": "PHPS",
		"example": "$PHPS$34323438373734$5b07e065b9d78d69603e71201c6cf29f",
	},
	{
		"code": "99999",
		"name": "Plaintext",
		"example": "hashcat",
	},
	{
		"code": "12",
		"name": "PostgreSQL",
		"example": "a6343a68d964ca596d9752250d54bb8a:postgres",
	},
	{
		"code": "11100",
		"name": "PostgreSQL Challenge-Response Authentication (MD5)",
		"example": "$postgres$postgres*f0784ea5*2091bb7d4725d1ca85e8de6ec349baf6",
	},
	{
		"code": "11000",
		"name": "PrestaShop",
		"example": "810e3d12f0f10777a679d9ca1ad7a8d9:M2uZ122bSHJ4Mi54tXGY0lqcv1r28mUluSkyw37ou5oia4i239ujqw0l",
	},
	{
		"code": "4522",
		"name": "PunBB",
		"example": "4a2b722cc65ecf0f7797cdaea4bce81f66716eef:653074362104",
	},
	{
		"code": "999999",
		"name": "pwdump",
		"example": "Administrator:500:F0D412BD764FFE81AAD3B435B51404EE:209C6174DA490CAEB422F3FA5A7AE634:::",
	},
	{
		"code": "8500",
		"name": "RACF",
		"example": "$racf$*USER*FC2577C6EBE6265B",
	},
	{
		"code": "9900",
		"name": "Radmin2",
		"example": "22527bee5c29ce95373c4e0f359f079b",
	},
	{
		"code": "12500",
		"name": "RAR3-hp",
		"example": "$RAR3$*0*45109af8ab5f297a*adbf6c5385d7a40373e8f77d7b89d317",
	},
	{
		"code": "13000",
		"name": "RAR5",
		"example": "$rar5$16$74575567518807622265582327032280$15$f8b4064de34ac02ecabfe9abdf93ed6a$8$9843834ed0f7c754",
	},
	{
		"code": "4521",
		"name": "Redmine Project Management Web App",
		"example": "1fb46a8f81d8838f46879aaa29168d08aa6bf22d:3290afd193d90e900e8021f81409d7a9",
	},
	{
		"code": "6000",
		"name": "RipeMD160",
		"example": "012cb9b334ec1aeb71a9c8ce85586082467f7eb6",
	},
	{
		"code": "5800",
		"name": "Samsung Android Password/PIN",
		"example": "0223b799d526b596fe4ba5628b9e65068227e68e:f6d45822728ddb2c",
	},
	{
		"code": "7700",
		"name": "SAP CODVN B (BCODE)",
		"example": "user$c8b48f26b87b7ea7",
	},
	{
		"code": "7800",
		"name": "SAP CODVN F/G (PASSCODE)",
		"example": "user$abcad719b17e7f794df7e686e563e9e2d24de1d0",
	},
	{
		"code": "10300",
		"name": "SAP CODVN H (PWDSALTEDHASH) iSSHA-1",
		"example": "{x-issha, 1024}C0624EvGSdAMCtuWnBBYBGA0chvqAflKY74oEpw/rpY=",
	},
	{
		"code": "8900",
		"name": "scrypt",
		"example": "SCRYPT:1024:1:1:MDIwMzMwNTQwNDQyNQ==:5FW+zWivLxgCWj7qLiQbeC8zaNQ+qdO0NUinvqyFcfo=",
	},
	{
		"code": "1300",
		"name": "SHA-224",
		"example": "e4fa1555ad877bf0ec455483371867200eee89550a93eff2f95a6198",
	},
	{
		"code": "5000",
		"name": "SHA-3(Keccak)",
		"example": "203f88777f18bb4ee1226627b547808f38d90d3e106262b5de9ca943b57137b6",
	},
	{
		"code": "100",
		"name": "SHA1",
		"example": "b89eaac7e61417341b710b727768294d0e6a277b",
	},
	{
		"code": "110",
		"name": "sha1($pass.$salt)",
		"example": "2fc5a684737ce1bf7b3b239df432416e0dd07357:2014",
	},
	{
		"code": "120",
		"name": "sha1($salt.$pass)",
		"example": "cac35ec206d868b7d7cb0b55f31d9425b075082b:5363620024",
	},
	{
		"code": "4900",
		"name": "sha1($salt.$pass.$salt)",
		"example": "85087a691a55cbb41ae335d459a9121d54080b80:488387841",
	},
	{
		"code": "4520",
		"name": "sha1($salt.sha1($pass))",
		"example": "a0f835fdf57d36ebd8d0399cc44e6c2b86a1072b:511358214352751667201107073531735211566650747315",
	},
	{
		"code": "140",
		"name": "sha1($salt.unicode($pass))",
		"example": "5db61e4cd8776c7969cfd62456da639a4c87683a:8763434884872",
	},
	{
		"code": "14400",
		"name": "sha1(CX)",
		"example": "fd9149fb3ae37085dc6ed1314449f449fbf77aba:87740665218240877702",
	},
	{
		"code": "4700",
		"name": "sha1(md5($pass))",
		"example": "92d85978d884eb1d99a51652b1139c8279fa8663",
	},
	{
		"code": "4500",
		"name": "sha1(sha1($pass))",
		"example": "3db9184f5da4e463832b086211af8d2314919951",
	},
	{
		"code": "4600",
		"name": "sha1(sha1(sha1($pass)))",
		"example": "dc57f246485e62d99a5110afc9264b4ccbfcf3cc",
	},
	{
		"code": "130",
		"name": "sha1(unicode($pass).$salt)",
		"example": "c57f6ac1b71f45a07dbd91a59fa47c23abcd87c2:631225",
	},
	{
		"code": "1400",
		"name": "SHA256",
		"example": "127e6fbfe24a750e72930c220a8e138275656b8e5d8f48a98c3c92df2caba935",
	},
	{
		"code": "1410",
		"name": "sha256($pass.$salt)",
		"example": "c73d08de890479518ed60cf670d17faa26a4a71f995c1dcc978165399401a6c4:53743528",
	},
	{
		"code": "1420",
		"name": "sha256($salt.$pass)",
		"example": "eb368a2dfd38b405f014118c7d9747fcc97f4f0ee75c05963cd9da6ee65ef498:560407001617",
	},
	{
		"code": "1440",
		"name": "sha256($salt.unicode($pass))",
		"example": "a4bd99e1e0aba51814e81388badb23ecc560312c4324b2018ea76393ea1caca9:12345678",
	},
	{
		"code": "1430",
		"name": "sha256(unicode($pass).$salt)",
		"example": "4cc8eb60476c33edac52b5a7548c2c50ef0f9e31ce656c6f4b213f901bc87421:890128",
	},
	{
		"code": "7400",
		"name": "sha256crypt, SHA256(Unix)",
		"example": "$5$rounds=5000$GX7BopJZJxPc/KEK$le16UF8I2Anb.rOrn22AUPWvzUETDGefUmAV8AZkGcD",
	},
	{
		"code": "10800",
		"name": "SHA384",
		"example": "07371af1ca1fca7c6941d2399f3610f1e392c56c6d73fddffe38f18c430a2817028dae1ef09ac683b62148a2c8757f42",
	},
	{
		"code": "1700",
		"name": "SHA512",
		"example": "82a9dda829eb7f8ffe9fbe49e45d47d2dad9664fbb7adf72492e3c81ebd3e29134d9bc12212bf83c6840f10e8246b9db54a4859b7ccd0123d86e5872c1e5082f",
	},
	{
		"code": "1710",
		"name": "sha512($pass.$salt)",
		"example": "e5c3ede3e49fb86592fb03f471c35ba13e8d89b8ab65142c9a8fdafb635fa2223c24e5558fd9313e8995019dcbec1fb584146b7bb12685c7765fc8c0d51379fd:6352283260",
	},
	{
		"code": "1720",
		"name": "sha512($salt.$pass)",
		"example": "976b451818634a1e2acba682da3fd6efa72adf8a7a08d7939550c244b237c72c7d42367544e826c0c83fe5c02f97c0373b6b1386cc794bf0d21d2df01bb9c08a:2613516180127",
	},
	{
		"code": "1740",
		"name": "sha512($salt.unicode($pass))",
		"example": "bae3a3358b3459c761a3ed40d34022f0609a02d90a0d7274610b16147e58ece00cd849a0bd5cf6a92ee5eb5687075b4e754324dfa70deca6993a85b2ca865bc8:1237015423",
	},
	{
		"code": "1730",
		"name": "sha512(unicode($pass).$salt)",
		"example": "13070359002b6fbb3d28e50fba55efcf3d7cc115fe6e3f6c98bf0e3210f1c6923427a1e1a3b214c1de92c467683f6466727ba3a51684022be5cc2ffcb78457d2:341351589",
	},
	{
		"code": "1800",
		"name": "sha512crypt, SHA512(Unix)",
		"example": "$6$52450745$k5ka2p8bFuSmoVT1tzOyyuaREkkKBcCNqoDKzYiJL9RaE8yMnPgh2XzzF0NDrUhgrcLwg78xs1w5pJiypEdFX/",
	},
	{
		"code": "11400",
		"name": "SIP digest authentication (MD5)",
		"example": "$sip$*192.168.100.100*192.168.100.121*username*asterisk*REGISTER*sip*192.168.100.121**2b01df0b****MD5*ad0520061ca07c120d7e8ce696a6df2d",
	},
	{
		"code": "10100",
		"name": "SipHash",
		"example": "ad61d78c06037cd9:2:4:81533218127174468417660201434054",
	},
	{
		"code": "14900",
		"name": "Skip32",
		"example": "c9350366:44630464",
	},
	{
		"code": "23",
		"name": "Skype",
		"example": "3af0389f093b181ae26452015f4ae728:user",
	},
	{
		"code": "121",
		"name": "SMF >= v1.1",
		"example": "ecf076ce9d6ed3624a9332112b1cd67b236fdd11:17782686",
	},
	{
		"code": "1411",
		"name": "SSHA-256(Base64), LDAP {SSHA256}",
		"example": "{SSHA256}OZiz0cnQ5hgyel3Emh7NCbhBRCQ+HVBwYplQunHYnER7TLuV",
	},
	{
		"code": "1711",
		"name": "SSHA-512(Base64), LDAP {SSHA512}",
		"example": "{SSHA512}ALtwKGBdRgD+U0fPAy31C28RyKYx7+a8kmfksccsOeLknLHv2DBXYI7TDnTolQMBuPkWDISgZr2cHfnNPFjGZTEyNDU4OTkw",
	},
	{
		"code": "8000",
		"name": "Sybase ASE",
		"example": "0xc00778168388631428230545ed2c976790af96768afa0806fe6c0da3b28f3e132137eac56f9bad027ea2",
	},
	{
		"code": "2611",
		"name": "vBulletin < v3.8.5",
		"example": "16780ba78d2d5f02f3202901c1b6d975:568",
	},
	{
		"code": "2711",
		"name": "vBulletin >= v3.8.5",
		"example": "bf366348c53ddcfbd16e63edfdd1eee6:181264250056774603641874043270",
	},
	{
		"code": "8400",
		"name": "WBB3, Woltlab Burning Board 3",
		"example": "8084df19a6dc81e2597d051c3d8b400787e2d5a9:6755045315424852185115352765375338838643",
	},
	{
		"code": "3721",
		"name": "WebEdition",
		"example": "fa01af9f0de5f377ae8befb03865178e:5678",
	},
	{
		"code": "6100",
		"name": "Whirlpool",
		"example": "7ca8eaaaa15eaa4c038b4c47b9313e92da827c06940e69947f85bc0fbef3eb8fd254da220ad9e208b6b28f6bb9be31dd760f1fdb26112d83f87d96b416a4d258",
	},
	{
		"code": "13800",
		"name": "Windows 8+ phone PIN/Password",
		"example": "95fc4680bcd2a5f25de3c580cbebadbbf256c1f0ff2e9329c58e36f8b914c11f:4471347156480581513210137061422464818088437334031753080747625028271635402815635172140161077854162657165115624364524648202480341513407048222056541500234214433548175101668212658151115765112202168288664210443352443335235337677853484573107775345675846323265745",
	},
	{
		"code": "13600",
		"name": "WinZip",
		"example": "$zip2$*0*3*0*b5d2b7bf57ad5e86a55c400509c672bd*d218*0**ca3d736d03a34165cfa9*$/zip2$",
	},
]

