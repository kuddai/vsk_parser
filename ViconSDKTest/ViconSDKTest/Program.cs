///////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) OMG Plc 2009.
// All rights reserved.  This software is protected by copyright
// law and international treaties.  No part of this software / document
// may be reproduced or distributed in any form or by any means,
// whether transiently or incidentally to some other use of this software,
// without the written permission of the copyright owner.
//
///////////////////////////////////////////////////////////////////////////////

using System;
using System.Collections.Generic;
using System.Text;
using ViconDataStreamSDK.DotNET;

namespace CSharpClient
{
    class Program
    {
        static string Adapt(Direction i_Direction)
        {
            switch (i_Direction)
            {
                case Direction.Forward:
                    return "Forward";
                case Direction.Backward:
                    return "Backward";
                case Direction.Left:
                    return "Left";
                case Direction.Right:
                    return "Right";
                case Direction.Up:
                    return "Up";
                case Direction.Down:
                    return "Down";
                default:
                    return "Unknown";
            }
        }

        static string Adapt(DeviceType i_DeviceType)
        {
            switch (i_DeviceType)
            {
                case DeviceType.ForcePlate:
                    return "ForcePlate";
                case DeviceType.Unknown:
                default:
                    return "Unknown";
            }
        }

        static string Adapt(Unit i_Unit)
        {
            switch (i_Unit)
            {
                case Unit.Meter:
                    return "Meter";
                case Unit.Volt:
                    return "Volt";
                case Unit.NewtonMeter:
                    return "NewtonMeter";
                case Unit.Newton:
                    return "Newton";
                case Unit.Kilogram:
                    return "Kilogram";
                case Unit.Second:
                    return "Second";
                case Unit.Ampere:
                    return "Ampere";
                case Unit.Kelvin:
                    return "Kelvin";
                case Unit.Mole:
                    return "Mole";
                case Unit.Candela:
                    return "Candela";
                case Unit.Radian:
                    return "Radian";
                case Unit.Steradian:
                    return "Steradian";
                case Unit.MeterSquared:
                    return "MeterSquared";
                case Unit.MeterCubed:
                    return "MeterCubed";
                case Unit.MeterPerSecond:
                    return "MeterPerSecond";
                case Unit.MeterPerSecondSquared:
                    return "MeterPerSecondSquared";
                case Unit.RadianPerSecond:
                    return "RadianPerSecond";
                case Unit.RadianPerSecondSquared:
                    return "RadianPerSecondSquared";
                case Unit.Hertz:
                    return "Hertz";
                case Unit.Joule:
                    return "Joule";
                case Unit.Watt:
                    return "Watt";
                case Unit.Pascal:
                    return "Pascal";
                case Unit.Lumen:
                    return "Lumen";
                case Unit.Lux:
                    return "Lux";
                case Unit.Coulomb:
                    return "Coulomb";
                case Unit.Ohm:
                    return "Ohm";
                case Unit.Farad:
                    return "Farad";
                case Unit.Weber:
                    return "Weber";
                case Unit.Tesla:
                    return "Tesla";
                case Unit.Henry:
                    return "Henry";
                case Unit.Siemens:
                    return "Siemens";
                case Unit.Becquerel:
                    return "Becquerel";
                case Unit.Gray:
                    return "Gray";
                case Unit.Sievert:
                    return "Sievert";
                case Unit.Katal:
                    return "Katal";

                case Unit.Unknown:
                default:
                    return "Unknown";
            }
        }

        static void Main(string[] args)
        {
            // Program options
            int Counter = 1;


            string HostName = "localhost:801";
            if (args.Length == 1)
            {
                HostName = args[0];
            }
            
            // Make a new client
            ViconDataStreamSDK.DotNET.Client MyClient = new ViconDataStreamSDK.DotNET.Client();

            // Connect to a server
            Console.Write("Connecting to {0:0.00} ...", HostName);
            while (!MyClient.IsConnected().Connected)
            {
                // Direct connection
                MyClient.Connect(HostName);

                // Multicast connection
                // MyClient.ConnectToMulticast( HostName, "224.0.0.0" );

                System.Threading.Thread.Sleep(200);
                Console.Write(".");
            }
            Console.WriteLine();

            // Enable some different data types
            MyClient.EnableSegmentData();
            MyClient.EnableMarkerData();
            MyClient.EnableUnlabeledMarkerData();
            MyClient.EnableDeviceData();

            Console.WriteLine("Segment Data Enabled: {0}", MyClient.IsSegmentDataEnabled().Enabled);
            Console.WriteLine("Marker Data Enabled: {0}", MyClient.IsMarkerDataEnabled().Enabled);
            Console.WriteLine("Unlabeled Marker Data Enabled: {0}", MyClient.IsUnlabeledMarkerDataEnabled().Enabled);
            Console.WriteLine("Device Data Enabled: {0}", MyClient.IsDeviceDataEnabled().Enabled);

            // Set the streaming mode
            MyClient.SetStreamMode(ViconDataStreamSDK.DotNET.StreamMode.ClientPull);
            // MyClient.SetStreamMode( ViconDataStreamSDK.DotNET.StreamMode.ClientPullPreFetch );
            // MyClient.SetStreamMode( ViconDataStreamSDK.DotNET.StreamMode.ServerPush );

            // Set the global up axis
            MyClient.SetAxisMapping(ViconDataStreamSDK.DotNET.Direction.Forward,
                                     ViconDataStreamSDK.DotNET.Direction.Left,
                                     ViconDataStreamSDK.DotNET.Direction.Up); // Z-up
                                                                              // MyClient.SetAxisMapping( ViconDataStreamSDK.DotNET.Direction.Forward, 
                                                                              //                          ViconDataStreamSDK.DotNET.Direction.Up, 
                                                                              //                          ViconDataStreamSDK.DotNET.Direction.Right ); // Y-up

            Output_GetAxisMapping _Output_GetAxisMapping = MyClient.GetAxisMapping();
            Console.WriteLine("Axis Mapping: X-{0} Y-{1} Z-{2}", Adapt(_Output_GetAxisMapping.XAxis),
                                                                  Adapt(_Output_GetAxisMapping.YAxis),
                                                                  Adapt(_Output_GetAxisMapping.ZAxis));

            // Discover the version number
            Output_GetVersion _Output_GetVersion = MyClient.GetVersion();
            Console.WriteLine("Version: {0}.{1}.{2}", _Output_GetVersion.Major,
                                                       _Output_GetVersion.Minor,
                                                       _Output_GetVersion.Point);


            // Loop until a key is pressed
            while (true)
            {
                ++Counter;
                // Console.KeyAvailable throws an exception if stdin is a pipe (e.g.
                // with TrackerDssdkTests.py), so we use try..catch:
                try
                {
                    if (Console.KeyAvailable)
                    {
                        break;
                    }
                }
                catch (InvalidOperationException)
                {
                }

                // Get a frame
                Console.Write("Waiting for new frame...");
                //MyClient.get
                while (MyClient.GetFrame().Result != ViconDataStreamSDK.DotNET.Result.Success)
                {
                    System.Threading.Thread.Sleep(200);
                    //Console.Write(".");
                }
                Console.WriteLine("\n\n\n\n\n");

                // Get the frame number
                Output_GetFrameNumber _Output_GetFrameNumber = MyClient.GetFrameNumber();
                Console.WriteLine("Frame Number: {0}", _Output_GetFrameNumber.FrameNumber + 1);

                Output_GetFrameRate _Output_GetFrameRate = MyClient.GetFrameRate();
                Console.WriteLine("Frame rate: {0}", _Output_GetFrameRate.FrameRateHz);


                // Get the timecode
                Output_GetTimecode _Output_GetTimecode = MyClient.GetTimecode();
                Console.WriteLine("Timecode: {0}h {1}m {2}s {3}f {4}sf {5} {6} {7} {8}",
                                   _Output_GetTimecode.Hours,
                                   _Output_GetTimecode.Minutes,
                                   _Output_GetTimecode.Seconds,
                                   _Output_GetTimecode.Frames,
                                   _Output_GetTimecode.SubFrame,
                                   _Output_GetTimecode.FieldFlag,
                                   _Output_GetTimecode.Standard.ToString("d"),
                                   _Output_GetTimecode.SubFramesPerFrame,
                                   _Output_GetTimecode.UserBits);
                Console.WriteLine();

                // Get the latency
                Console.WriteLine("Latency: {0}s", MyClient.GetLatencyTotal().Total);

                for (uint LatencySampleIndex = 0; LatencySampleIndex < MyClient.GetLatencySampleCount().Count; ++LatencySampleIndex)
                {
                    string SampleName = MyClient.GetLatencySampleName(LatencySampleIndex).Name;
                    double SampleValue = MyClient.GetLatencySampleValue(SampleName).Value;

                    Console.WriteLine("  {0} {1}s", SampleName, SampleValue);
                }
                Console.WriteLine();


                // Count the number of subjects
                uint SubjectCount = MyClient.GetSubjectCount().SubjectCount;
                Console.WriteLine("Subjects ({0}):", SubjectCount);
                for (uint SubjectIndex = 0; SubjectIndex < SubjectCount; ++SubjectIndex)
                {
                    Console.WriteLine("  Subject #{0}", SubjectIndex);

                    // Get the subject name
                    string SubjectName = MyClient.GetSubjectName(SubjectIndex).SubjectName;
                    Console.WriteLine("    Name: {0}", SubjectName);

                    // Get the root segment
                    string RootSegment = MyClient.GetSubjectRootSegmentName(SubjectName).SegmentName;
                    Console.WriteLine("    Root Segment: {0}", RootSegment);

                    // Count the number of segments
                    uint SegmentCount = MyClient.GetSegmentCount(SubjectName).SegmentCount;
                    Console.WriteLine("    Segments ({0}):", SegmentCount);
                    for (uint SegmentIndex = 0; SegmentIndex < SegmentCount; ++SegmentIndex)
                    {
                        Console.WriteLine("      Segment #{0}", SegmentIndex);

                        // Get the segment name
                        string SegmentName = MyClient.GetSegmentName(SubjectName, SegmentIndex).SegmentName;
                        Console.WriteLine("        Name: {0}", SegmentName);

                        // Get the segment parent
                        string SegmentParentName = MyClient.GetSegmentParentName(SubjectName, SegmentName).SegmentName;
                        Console.WriteLine("        Parent: {0}", SegmentParentName);

                        // Get the segment's children
                        uint ChildCount = MyClient.GetSegmentChildCount(SubjectName, SegmentName).SegmentCount;
                        Console.WriteLine("     Children ({0}):", ChildCount);
                        for (uint ChildIndex = 0; ChildIndex < ChildCount; ++ChildIndex)
                        {
                            string ChildName = MyClient.GetSegmentChildName(SubjectName, SegmentName, ChildIndex).SegmentName;
                            Console.WriteLine("       {0}", ChildName);
                        }

                        // Get the static segment translation
                        Output_GetSegmentStaticTranslation _Output_GetSegmentStaticTranslation =
                          MyClient.GetSegmentStaticTranslation(SubjectName, SegmentName);
                        Console.WriteLine("        Static Translation: ({0:0.00},{1:0.00},{2:0.00})",
                                           _Output_GetSegmentStaticTranslation.Translation[0],
                                           _Output_GetSegmentStaticTranslation.Translation[1],
                                           _Output_GetSegmentStaticTranslation.Translation[2]);

                        // Get the static segment rotation in helical co-ordinates
                        Output_GetSegmentStaticRotationHelical _Output_GetSegmentStaticRotationHelical =
                          MyClient.GetSegmentStaticRotationHelical(SubjectName, SegmentName);
                        Console.WriteLine("        Static Rotation Helical: ({0:0.00},{1:0.00},{2:0.00})",
                                           _Output_GetSegmentStaticRotationHelical.Rotation[0],
                                           _Output_GetSegmentStaticRotationHelical.Rotation[1],
                                           _Output_GetSegmentStaticRotationHelical.Rotation[2]);

                        // Get the static segment rotation as a matrix
                        Output_GetSegmentStaticRotationMatrix _Output_GetSegmentStaticRotationMatrix =
                          MyClient.GetSegmentStaticRotationMatrix(SubjectName, SegmentName);
                        Console.WriteLine("        Static Rotation Matrix: ({0:0.00},{1:0.00},{2:0.00},{3:0.00},{4:0.00},{5:0.00},{6:0.00},{7:0.00},{8:0.00})",
                                           _Output_GetSegmentStaticRotationMatrix.Rotation[0],
                                           _Output_GetSegmentStaticRotationMatrix.Rotation[1],
                                           _Output_GetSegmentStaticRotationMatrix.Rotation[2],
                                           _Output_GetSegmentStaticRotationMatrix.Rotation[3],
                                           _Output_GetSegmentStaticRotationMatrix.Rotation[4],
                                           _Output_GetSegmentStaticRotationMatrix.Rotation[5],
                                           _Output_GetSegmentStaticRotationMatrix.Rotation[6],
                                           _Output_GetSegmentStaticRotationMatrix.Rotation[7],
                                           _Output_GetSegmentStaticRotationMatrix.Rotation[8]);

                        // Get the static segment rotation in EulerXYZ co-ordinates
                        Output_GetSegmentStaticRotationEulerXYZ _Output_GetSegmentStaticRotationEulerXYZ =
                          MyClient.GetSegmentStaticRotationEulerXYZ(SubjectName, SegmentName);
                        Console.WriteLine("        Static Rotation EulerXYZ: ({0:0.00},{1:0.00},{2:0.00})",
                                           _Output_GetSegmentStaticRotationEulerXYZ.Rotation[0],
                                           _Output_GetSegmentStaticRotationEulerXYZ.Rotation[1],
                                           _Output_GetSegmentStaticRotationEulerXYZ.Rotation[2]);

                        // Get the global segment translation
                        Output_GetSegmentGlobalTranslation _Output_GetSegmentGlobalTranslation =
                          MyClient.GetSegmentGlobalTranslation(SubjectName, SegmentName);
                        Console.WriteLine("        Global Translation: ({0:0.00},{1:0.00},{2:0.00}) {3}",
                                           _Output_GetSegmentGlobalTranslation.Translation[0],
                                           _Output_GetSegmentGlobalTranslation.Translation[1],
                                           _Output_GetSegmentGlobalTranslation.Translation[2],
                                           _Output_GetSegmentGlobalTranslation.Occluded);

                        // Get the global segment rotation in helical co-ordinates
                        Output_GetSegmentGlobalRotationHelical _Output_GetSegmentGlobalRotationHelical =
                          MyClient.GetSegmentGlobalRotationHelical(SubjectName, SegmentName);
                        Console.WriteLine("        Global Rotation Helical: ({0:0.00},{1:0.00},{2:0.00}) {3}",
                                           _Output_GetSegmentGlobalRotationHelical.Rotation[0],
                                           _Output_GetSegmentGlobalRotationHelical.Rotation[1],
                                           _Output_GetSegmentGlobalRotationHelical.Rotation[2],
                                           _Output_GetSegmentGlobalRotationHelical.Occluded);

                        // Get the global segment rotation as a matrix
                        Output_GetSegmentGlobalRotationMatrix _Output_GetSegmentGlobalRotationMatrix =
                          MyClient.GetSegmentGlobalRotationMatrix(SubjectName, SegmentName);
                        Console.WriteLine("        Global Rotation Matrix: ({0:0.00},{1:0.00},{2:0.00},{3:0.00},{4:0.00},{5:0.00},{6:0.00},{7:0.00},{8:0.00}) {9}",
                                           _Output_GetSegmentGlobalRotationMatrix.Rotation[0],
                                           _Output_GetSegmentGlobalRotationMatrix.Rotation[1],
                                           _Output_GetSegmentGlobalRotationMatrix.Rotation[2],
                                           _Output_GetSegmentGlobalRotationMatrix.Rotation[3],
                                           _Output_GetSegmentGlobalRotationMatrix.Rotation[4],
                                           _Output_GetSegmentGlobalRotationMatrix.Rotation[5],
                                           _Output_GetSegmentGlobalRotationMatrix.Rotation[6],
                                           _Output_GetSegmentGlobalRotationMatrix.Rotation[7],
                                           _Output_GetSegmentGlobalRotationMatrix.Rotation[8],
                                           _Output_GetSegmentGlobalRotationMatrix.Occluded);
                        

                        // Get the global segment rotation in EulerXYZ co-ordinates
                        Output_GetSegmentGlobalRotationEulerXYZ _Output_GetSegmentGlobalRotationEulerXYZ =
                          MyClient.GetSegmentGlobalRotationEulerXYZ(SubjectName, SegmentName);
                        Console.WriteLine("        Global Rotation EulerXYZ: ({0:0.00},{1:0.00},{2:0.00}) {3}",
                                           _Output_GetSegmentGlobalRotationEulerXYZ.Rotation[0],
                                           _Output_GetSegmentGlobalRotationEulerXYZ.Rotation[1],
                                           _Output_GetSegmentGlobalRotationEulerXYZ.Rotation[2],
                                           _Output_GetSegmentGlobalRotationEulerXYZ.Occluded);

                        // Get the local segment translation
                        Output_GetSegmentLocalTranslation _Output_GetSegmentLocalTranslation =
                          MyClient.GetSegmentLocalTranslation(SubjectName, SegmentName);
                        Console.WriteLine("        Local Translation: ({0:0.00},{1:0.00},{2:0.00}) {3}",
                                           _Output_GetSegmentLocalTranslation.Translation[0],
                                           _Output_GetSegmentLocalTranslation.Translation[1],
                                           _Output_GetSegmentLocalTranslation.Translation[2],
                                           _Output_GetSegmentLocalTranslation.Occluded);

                        // Get the local segment rotation in helical co-ordinates
                        Output_GetSegmentLocalRotationHelical _Output_GetSegmentLocalRotationHelical =
                          MyClient.GetSegmentLocalRotationHelical(SubjectName, SegmentName);
                        Console.WriteLine("        Local Rotation Helical: ({0:0.00},{1:0.00},{2:0.00}) {3}",
                                           _Output_GetSegmentLocalRotationHelical.Rotation[0],
                                           _Output_GetSegmentLocalRotationHelical.Rotation[1],
                                           _Output_GetSegmentLocalRotationHelical.Rotation[2],
                                           _Output_GetSegmentLocalRotationHelical.Occluded);

                        // Get the local segment rotation as a matrix
                        Output_GetSegmentLocalRotationMatrix _Output_GetSegmentLocalRotationMatrix =
                          MyClient.GetSegmentLocalRotationMatrix(SubjectName, SegmentName);
                        Console.WriteLine("        Local Rotation Matrix: ({0:0.00},{1:0.00},{2:0.00},{3:0.00},{4:0.00},{5:0.00},{6:0.00},{7:0.00},{8:0.00}) {9}",
                                           _Output_GetSegmentLocalRotationMatrix.Rotation[0],
                                           _Output_GetSegmentLocalRotationMatrix.Rotation[1],
                                           _Output_GetSegmentLocalRotationMatrix.Rotation[2],
                                           _Output_GetSegmentLocalRotationMatrix.Rotation[3],
                                           _Output_GetSegmentLocalRotationMatrix.Rotation[4],
                                           _Output_GetSegmentLocalRotationMatrix.Rotation[5],
                                           _Output_GetSegmentLocalRotationMatrix.Rotation[6],
                                           _Output_GetSegmentLocalRotationMatrix.Rotation[7],
                                           _Output_GetSegmentLocalRotationMatrix.Rotation[8],
                                           _Output_GetSegmentLocalRotationMatrix.Occluded);

                        // Get the local segment rotation in EulerXYZ co-ordinates
                        Output_GetSegmentLocalRotationEulerXYZ _Output_GetSegmentLocalRotationEulerXYZ =
                          MyClient.GetSegmentLocalRotationEulerXYZ(SubjectName, SegmentName);
                        Console.WriteLine("        Local Rotation EulerXYZ: ({0:0.00},{1:0.00},{2:0.00}) {3}",
                                           _Output_GetSegmentLocalRotationEulerXYZ.Rotation[0],
                                           _Output_GetSegmentLocalRotationEulerXYZ.Rotation[1],
                                           _Output_GetSegmentLocalRotationEulerXYZ.Rotation[2],
                                           _Output_GetSegmentLocalRotationEulerXYZ.Occluded);
                    }
                    
                }

            }
            

            // Disconnect and dispose
            MyClient.Disconnect();
            MyClient = null;
        }
    }
}
