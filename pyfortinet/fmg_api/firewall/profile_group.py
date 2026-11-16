"""Firewall security profile groups."""

from typing import Optional

from pydantic import AliasChoices, Field

from pyfortinet.fmg_api import FMGObject


class ProfileGroup(FMGObject):
    """Service group class

    Attributes:
        application_list: Name of an existing Application list.
        av_profile: Name of an existing Antivirus profile.
        dlp_profile: Name of an existing DLP profile.
        dnsfilter_profile: Name of an existing DNS filter profile.
        emailfilter_profile: Name of an existing email filter profile.
        file_filter_profile: Name of an existing file_filter profile.
        icap_profile: Name of an existing ICAP profile.
        ips_sensor: Name of an existing IPS sensor.
        ips_voip_filter: Name of an existing VoIP (ips) profile.
        name: Profile group name.
        profile_protocol_options: Name of an existing Protocol options profile.
        sctp_filter_profile: Name of an existing SCTP filter profile.
        ssh_filter_profile: Name of an existing SSH filter profile.
        ssl_ssh_profile: Name of an existing SSL SSH profile.
        videofilter_profile: Name of an existing VideoFilter profile.
        voip_profile: Name of an existing VoIP (voipd) profile.
        waf_profile: Name of an existing Web application firewall profile.
        webfilter_profile: Name of an existing Web filter profile.
    """

    _url = "/pm/config/{scope}/obj/firewall/profile-group/{profile_group}"
    _master_keys = {"profile_group": "name"}
    application_list: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("application-list", "application_list"),
        serialization_alias="application-list",
    )
    av_profile: Optional[str] = Field(
        None, validation_alias=AliasChoices("av-profile", "av_profile"), serialization_alias="av-profile"
    )
    dlp_profile: Optional[str] = Field(
        None, validation_alias=AliasChoices("dlp-profile", "dlp_profile"), serialization_alias="dlp-profile"
    )
    dnsfilter_profile: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("dnsfilter-profile", "dnsfilter_profile"),
        serialization_alias="dnsfilter-profile",
    )
    emailfilter_profile: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("emailfilter-profile", "emailfilter_profile"),
        serialization_alias="emailfilter-profile",
    )
    file_filter_profile: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("file-filter-profile", "file_filter_profile"),
        serialization_alias="file-filter-profile",
    )
    icap_profile: Optional[str] = Field(
        None, validation_alias=AliasChoices("icap-profile", "icap_profile"), serialization_alias="icap-profile"
    )
    ips_sensor: Optional[str] = Field(
        None, validation_alias=AliasChoices("ips-sensor", "ips_sensor"), serialization_alias="ips-sensor"
    )
    ips_voip_filter: Optional[str] = Field(
        None, validation_alias=AliasChoices("ips-voip-filter", "ips_voip_filter"), serialization_alias="ips-voip-filter"
    )
    name: Optional[str] = None
    profile_protocol_options: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("profile-protocol-options", "profile_protocol_options"),
        serialization_alias="profile-protocol-options",
    )
    sctp_filter_profile: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("sctp-filter-profile", "sctp_filter_profile"),
        serialization_alias="sctp-filter-profile",
    )
    ssh_filter_profile: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ssh-filter-profile", "ssh_filter_profile"),
        serialization_alias="ssh-filter-profile",
    )
    ssl_ssh_profile: Optional[str] = Field(
        None, validation_alias=AliasChoices("ssl-ssh-profile", "ssl_ssh_profile"), serialization_alias="ssl-ssh-profile"
    )
    videofilter_profile: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("videofilter-profile", "videofilter_profile"),
        serialization_alias="videofilter-profile",
    )
    voip_profile: Optional[str] = Field(
        None, validation_alias=AliasChoices("voip-profile", "voip_profile"), serialization_alias="voip-profile"
    )
    waf_profile: Optional[str] = Field(
        None, validation_alias=AliasChoices("waf-profile", "waf_profile"), serialization_alias="waf-profile"
    )
    webfilter_profile: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("webfilter-profile", "webfilter_profile"),
        serialization_alias="webfilter-profile",
    )
