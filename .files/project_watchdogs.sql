PGDMP     &                    y            Project_Watchdogs    13.1    13.1     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16394    Project_Watchdogs    DATABASE     w   CREATE DATABASE "Project_Watchdogs" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_United States.1252';
 #   DROP DATABASE "Project_Watchdogs";
                postgres    false                        2615    16395    Data    SCHEMA        CREATE SCHEMA "Data";
    DROP SCHEMA "Data";
                postgres    false            �            1259    16396    Scans    TABLE     �   CREATE TABLE "Data"."Scans" (
    id uuid NOT NULL,
    device_name text,
    ip_address text NOT NULL,
    mac_address text,
    type integer NOT NULL
);
    DROP TABLE "Data"."Scans";
       Data         heap    postgres    false    6            �          0    16396    Scans 
   TABLE DATA           Q   COPY "Data"."Scans" (id, device_name, ip_address, mac_address, type) FROM stdin;
    Data          postgres    false    201   5       #           2606    16403    Scans Scans_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY "Data"."Scans"
    ADD CONSTRAINT "Scans_pkey" PRIMARY KEY (id);
 >   ALTER TABLE ONLY "Data"."Scans" DROP CONSTRAINT "Scans_pkey";
       Data            postgres    false    201            �      x������ � �     